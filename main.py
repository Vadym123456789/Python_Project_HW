from flask import Flask, session, redirect, url_for, render_template, request, flash, jsonify
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key'


def get_db():
    db = sqlite3.connect('database_project2/database_Project2.db')
    db.row_factory = sqlite3.Row
    return db


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_login' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Допоміжні функції для роботи з БД
def get_user(login):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM User WHERE login = ?', (login,))
    return cursor.fetchone()


def create_user(login, password, ipn=None, full_name=None, contacts=None):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute('''
            INSERT INTO User (login, password, ipn, full_name, contacts)
            VALUES (?, ?, ?, ?, ?)
        ''', (login, password, ipn, full_name, contacts))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
        return False


# Маршрути
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = get_user(login)

        if user and check_password_hash(user['password'], password):
            session['user_login'] = login
            return redirect(url_for('items'))
        else:
            flash('Невірний логін або пароль')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form

        if not all(key in data for key in ['login', 'password']):
            flash('Відсутні обов\'язкові поля')
            return render_template('register.html')

        existing_user = get_user(data['login'])
        if existing_user:
            flash('Користувач з таким логіном вже існує')
            return render_template('register.html')

        hashed_password = generate_password_hash(data['password'])
        success = create_user(
            login=data['login'],
            password=hashed_password,
            full_name=data.get('full_name'),
            contacts=data.get('contacts')
        )

        if success:
            flash('Реєстрація успішна!')
            return redirect(url_for('login'))
        else:
            flash('Помилка при реєстрації')

    return render_template('register.html')


@app.route('/items')
@login_required
def items():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Item')
    items = cursor.fetchall()
    return render_template('items.html', items=items)


@app.route('/items/<int:item_id>')
@login_required
def get_item(item_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Item WHERE item_id = ?', (item_id,))
    item = cursor.fetchone()
    if item is None:
        return 'Item not found', 404
    return jsonify(dict(item))


@app.route('/logout')
def logout():
    session.pop('user_login', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)