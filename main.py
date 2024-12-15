import os
import logging
from functools import wraps
from datetime import datetime

from flask import (
    Flask,
    redirect,
    url_for,
    render_template,
    request,
    flash,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)

from models import Item, User, Contract, Session
from celery_app import send_contract_email
from config import Config
from celery import Celery

# Налаштування логування
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Визначення шляху до бази даних
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = r"C:\Users\vgumenyuk1\Documents\Python projects\pythonProject 2\database_project2\database_Project2.db"

# Створення застосунку Flask та Celery
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app


def create_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY"]["broker_url"],
        backend=app.config["CELERY"]["result_backend"],
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = create_app()
celery = create_celery(app)

# Ініціалізація Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    with Session() as session:
        return session.get(User, int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")

        if not login or not password:
            flash("Будь ласка, введіть логін та пароль")
            return render_template("login.html")

        with Session() as session:
            user = session.query(User).filter(User.login == login).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("items_list"))
            else:
                flash("Невірний логін або пароль")
                return render_template("login.html")

    return render_template("login.html")


def get_user(login):
    logger.debug(f"Searching for user: {login}")
    try:
        with Session() as session:
            user = session.query(User).filter(User.login == login).first()
            if user:
                return user
        return None
    except Exception as e:
        logger.error(f"Error searching for user: {str(e)}")
        return None


def create_user(login, password, full_name=None, contacts=None, ipn=None):
    logger.debug(f"Attempting to create user: {login}")
    try:
        with Session() as session:
            new_user = User(
                login=login,
                password=password,
                full_name=full_name,
                contacts=contacts,
                ipn=ipn,
            )
            session.add(new_user)
            session.commit()
            logger.info(f"User {login} created successfully")
            return True
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return False


@app.route("/")
def index():
    return redirect(url_for("login"))


def get_all_items():
    try:
        with Session() as session:
            items = session.query(Item).all()
            return items
    except Exception as e:
        logger.error(f"Error getting items: {str(e)}")
        return []


@app.route("/register", methods=["GET", "POST"])
def register():
    logger.debug("=== Registration page opened ===")
    if request.method == "POST":
        logger.debug("=== Received POST request ===")
        try:
            data = request.form
            logger.debug(f"Form data: {dict(data)}")

            if not all(key in data for key in ["login", "password"]):
                logger.warning("Missing required fields")
                flash("Відсутні обов'язкові поля")
                return render_template("register.html")

            logger.debug(f"Checking user: {data['login']}")
            existing_user = get_user(data["login"])
            if existing_user:
                logger.warning(f"User {data['login']} already exists")
                flash("Користувач з таким логіном вже існує")
                return render_template("register.html")

            logger.debug("Hashing password...")
            hashed_password = generate_password_hash(data["password"])

            logger.debug("Attempting to create user...")
            success = create_user(
                login=data["login"],
                password=hashed_password,
                full_name=data.get("full_name"),
                contacts=data.get("contacts"),
            )

            if success:
                logger.info("Registration successful!")
                flash("Реєстрація успішна!")
                return redirect(url_for("login"))
            else:
                logger.error("Failed to create user")
                flash("Помилка при реєстрації")
        except Exception as e:
            logger.error(f"Critical error during registration: {str(e)}")
            flash("Помилка при реєстрації")
    else:
        logger.debug("GET request - showing registration form")
    return render_template("register.html")


@app.route("/items", endpoint="items_list")
@login_required
def items_list():
    try:
        items_list = get_all_items()
        return render_template("items.html", items=items_list)
    except Exception as e:
        logger.error(f"Error displaying items: {str(e)}")
        flash("Помилка при відображенні списку товарів")
        return redirect(url_for("login"))


@app.route("/items/<int:item_id>")
@login_required
def get_item(item_id):
    try:
        with Session() as session:
            item = session.get(Item, item_id)
            if not item:
                return "Item not found", 404

            return render_template("item.html", item=item)

    except Exception as e:
        logger.error(f"Error fetching item: {e}")
        return "Error fetching item", 500


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/edit_item/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    try:
        with Session() as session:
            item = session.get(Item, item_id)  # Використовуємо session.get()
            if not item:
                flash("Товар не знайдено")
                return redirect(url_for("items_list"))

            if request.method == "POST":
                item.name = request.form["name"]
                item.description = request.form.get("description")
                item.price_hour = (
                    float(request.form["price_hour"])
                    if request.form.get("price_hour")
                    else None
                )
                item.price_day = (
                    float(request.form["price_day"])
                    if request.form.get("price_day")
                    else None
                )
                item.price_week = (
                    float(request.form["price_week"])
                    if request.form.get("price_week")
                    else None
                )
                item.price_month = (
                    float(request.form["price_month"])
                    if request.form.get("price_month")
                    else None
                )
                session.commit()
                flash("Товар успішно оновлено")
                return redirect(url_for("items_list"))

            return render_template("edit_item.html", item=item)
    except Exception as e:
        app.logger.error(f"Error updating item: {str(e)}")
        flash("Error updating item", "error")
        return redirect(url_for("items_list"))


@app.route("/add_item", methods=["GET", "POST"])
@login_required
def add_item():
    if request.method == "POST":
        try:
            with Session() as session:
                new_item = Item(
                    name=request.form["name"],
                    description=request.form.get("description"),
                    price_hour=float(request.form["price_hour"])
                    if request.form.get("price_hour")
                    else None,
                    price_day=float(request.form["price_day"])
                    if request.form.get("price_day")
                    else None,
                    price_week=float(request.form["price_week"])
                    if request.form.get("price_week")
                    else None,
                    price_month=float(request.form["price_month"])
                    if request.form.get("price_month")
                    else None,
                )
                session.add(new_item)
                session.commit()
                flash("Товар успішно додано")
                return redirect(url_for("items_list"))
        except Exception as e:
            logger.error(f"Error adding item: {e}")
            flash("Помилка при додаванні товару")
    return render_template("add_item.html")


@app.route("/delete_item/<int:item_id>")
@login_required
def delete_item(item_id):
    try:
        with Session() as session:
            item = session.query(Item).get(item_id)
            if item:
                session.delete(item)
                session.commit()
                flash("Товар успішно видалено")
            else:
                flash("Товар не знайдено")
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}")
        flash(f"Помилка при видаленні товару: {str(e)}")

    return redirect(url_for("items_list"))


@app.route("/create_contract/<int:item_id>", methods=["GET", "POST"])
@login_required
def create_contract(item_id):
    try:
        with Session() as session:
            item = session.get(Item, item_id)
            if not item:
                flash("Товар не знайдено")
                return redirect(url_for("items_list"))

            if request.method == "POST":
                start_date_str = request.form["start_date"]
                end_date_str = request.form["end_date"]

                try:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                except ValueError:
                    flash("Невірний формат дати. Використовуйте YYYY-MM-DD")
                    return render_template("create_contract.html", item=item)

                price = int(request.form["price"])

                new_contract = Contract(
                    item_id=item_id,
                    user_id=current_user.id,
                    start_date=start_date,
                    end_date=end_date,
                    price=price,
                )
                session.add(new_contract)
                session.commit()

                # Надсилання email через Celery
                contract_info = {
                    "contract_id": new_contract.id,
                    "item_name": new_contract.item.name,
                    # ... інша інформація про контракт
                }
                send_contract_email.delay(contract_info)

                flash("Контракт успішно створено")
                return redirect(url_for("contracts"))

            return render_template("create_contract.html", item=item)
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating contract: {str(e)}")
        flash("Помилка при створенні контракту", "error")
        return redirect(url_for("items_list"))


@app.route("/contracts")
@login_required
def contracts():
    try:
        with Session() as session:
            contracts = (
                session.query(Contract)
                .filter(Contract.user_id == current_user.id)
                .all()
            )
            return render_template("contracts.html", contracts=contracts)
    except Exception as e:
        logger.error(f"Error fetching contracts: {str(e)}")
        flash(f"Помилка при отриманні контрактів: {str(e)}")
        return redirect(url_for("items_list"))


@app.route("/edit_contract/<int:contract_id>", methods=["GET", "POST"])
@login_required
def edit_contract(contract_id):
    try:
        with Session() as session:
            contract = session.query(Contract).get(contract_id)
            if not contract:
                flash("Контракт не знайдено")
                return redirect(url_for("contracts"))

            if request.method == "POST":
                start_date_str = request.form["start_date"]
                end_date_str = request.form["end_date"]
                price = int(request.form["price"])

                try:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                except ValueError:
                    flash("Невірний формат дати. Використовуйте YYYY-MM-DD")
                    return render_template("edit_contract.html", contract=contract)

                contract.start_date = start_date
                contract.end_date = end_date
                contract.price = price
                session.commit()

                flash("Контракт успішно оновлено")
                return redirect(url_for("contracts"))

            return render_template("edit_contract.html", contract=contract)
    except Exception as e:
        logger.error(f"Error editing contract: {str(e)}")
        flash(f"Помилка при редагуванні контракту: {str(e)}")
        return redirect(url_for("contracts"))


@app.route("/delete_contract/<int:contract_id>")
@login_required
def delete_contract(contract_id):
    try:
        with Session() as session:
            contract = session.query(Contract).get(contract_id)
            if not contract:
                flash("Контракт не знайдено")
                return redirect(url_for("contracts"))

            session.delete(contract)
            session.commit()
            flash("Контракт успішно видалено")
            return redirect(url_for("contracts"))
    except Exception as e:
        logger.error(f"Error deleting contract: {str(e)}")
        flash(f"Помилка при видаленні контракту: {str(e)}")
        return redirect(url_for("contracts"))


if __name__ == "__main__":
    logger.info("Starting Flask server...")

# Start the Flask application
app.run(host="0.0.0.0", port=5000, debug=True)