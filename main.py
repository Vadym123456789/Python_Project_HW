import os
import sqlite3
import logging
from functools import wraps

from flask import (
    Flask,
    session,
    redirect,
    url_for,
    render_template,
    request,
    flash,
    jsonify,
)
from werkzeug.security import generate_password_hash, check_password_hash

from database_project2.db_setup import DatabaseManager
from models import Item, Session, User

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


# Додайте нову функцію init_db
def init_db():
    logger.info("Initializing database...")
    try:
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

        with sqlite3.connect(DATABASE) as db:
            with open("schema.sql", "r", encoding="utf-8") as f:
                sql_script = f.read()
                db.executescript(sql_script)
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def get_db():
    try:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        return db
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Генеруємо безпечний секретний ключ


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_login" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def get_user(login):
    logger.debug(f"Searching for user: {login}")
    try:
        session = Session()
        user = session.query(User).filter(User.login == login).first()
        session.close()
        return user.__dict__ if user else None
    except Exception as e:
        logger.error(f"Error searching for user: {str(e)}")
        return None


def create_user(login, password, full_name=None, contacts=None, ipn=None):
    logger.debug(f"Attempting to create user: {login}")
    try:
        session = Session()
        new_user = User(login=login, password=password, full_name=full_name,
                        contacts=contacts, ipn=ipn)
        session.add(new_user)
        session.commit()
        session.close()
        logger.info(f"User {login} created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return False


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]

        user = get_user(login)

        if user and check_password_hash(user["password"], password):
            session["user_login"] = login
            return redirect(url_for("items"))
        else:
            flash("Невірний логін або пароль")

    return render_template("login.html")


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

            # TODO: Додати валідацію даних

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


@app.route("/items")
@login_required
def items():
    session = Session()
    items = session.query(Item).all()
    session.close()
    return render_template("items.html", items=items)


@app.route('/items/<int:item_id>')
@login_required
def get_item(item_id):
    try:
        session = Session()
        item = session.query(Item).filter(Item.id == item_id).first()
        session.close()
        if not item:
            return 'Item not found', 404

        item_dict = {c.name: getattr(item, c.name) for c in item.__table__.columns}  # Конвертуємо об'єкт Item в словник
        return jsonify(item_dict)

    except Exception as e:
        logger.error(f"Error fetching item: {e}")
        return 'Error fetching item', 500


@app.route("/logout")
def logout():
    session.pop("user_login", None)
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    user_login = session["user_login"]
    user_data = get_user(user_login)
    return render_template("profile.html", user=user_data)


if __name__ == "__main__":
    logger.info("Starting Flask server...")

    # Перевіряємо наявність бази даних
    if not os.path.exists(DATABASE):
        logger.warning("Database file not found, creating new database")
        try:
            init_db()
        except Exception as e:
            logger.error(f"Failed to create database: {e}")
            exit(1)

    # Перевіряємо чи можна підключитися до бази даних
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            logger.info(
                f"Connected to database. Found tables: {[table[0] for table in tables]}"
            )
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        logger.info("Attempting to reinitialize database...")
        try:
            os.remove(DATABASE)
            init_db()
        except Exception as e:
            logger.error(f"Failed to reinitialize database: {e}")
            exit(1)

    app.run(debug=True)