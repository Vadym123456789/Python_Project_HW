from flask import Flask, request, jsonify
from database_project2.db_setup import create_user, get_user, get_all_items, create_item, get_item_by_id
from werkzeug.security import generate_password_hash, check_password_hash

# Створюємо екземпляр Flask застосунку
app = Flask(__name__)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Повертаємо HTML форму для реєстрації
        return '''
            <form method="POST">
                <div>
                    <label>Login:</label>
                    <input type="text" name="login" required>
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" name="password" required>
                </div>
                <div>
                    <label>Full Name:</label>
                    <input type="text" name="full_name">
                </div>
                <div>
                    <label>Contacts:</label>
                    <input type="text" name="contacts">
                </div>
                <button type="submit">Register</button>
            </form>
        '''

    if request.method == 'POST':
        # Перевіряємо, чи дані прийшли як JSON
        if request.is_json:
            data = request.get_json()
        else:
            # Якщо дані прийшли з форми
            data = {
                'login': request.form.get('login'),
                'password': request.form.get('password'),
                'full_name': request.form.get('full_name'),
                'contacts': request.form.get('contacts')
            }

        # Перевіряємо наявність обов'язкових полів
        if not all(key in data for key in ['login', 'password']):
            return jsonify({
                'error': 'Відсутні обов\'язкові поля (login, password)'
            }), 400

        # Перевіряємо чи користувач вже існує
        existing_user = get_user(data['login'])
        if existing_user:
            return jsonify({
                'error': 'Користувач з таким логіном вже існує'
            }), 400

        # Хешуємо пароль для безпеки
        hashed_password = generate_password_hash(data['password'])

        # Створюємо користувача
        success = create_user(
            login=data['login'],
            password=hashed_password,
            ipn=data.get('ipn'),
            full_name=data.get('full_name'),
            contacts=data.get('contacts')
        )

        if success:
            return jsonify({
                'message': 'Користувач успішно зареєстрований',
                'login': data['login']
            }), 201
        else:
            return jsonify({
                'error': 'Помилка при створенні користувача'
            }), 500


# Отримання списку товарів
@app.route('/items', methods=['GET'])
def get_items():
    items = get_all_items()
    return jsonify(items), 200


# Отримання конкретного товару
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = get_item_by_id(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({'error': 'Товар не знайдено'}), 404


# Створення нового товару
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()

    # Перевіряємо наявність обов'язкових полів
    if 'name' not in data:
        return jsonify({
            'error': 'Відсутнє обов\'язкове поле name'
        }), 400

    # Створюємо товар
    item_id = create_item(
        name=data['name'],
        description=data.get('description'),
        price_hour=data.get('price_hour'),
        price_day=data.get('price_day'),
        price_week=data.get('price_week'),
        price_month=data.get('price_month')
    )

    if item_id:
        return jsonify({
            'message': 'Товар успішно створено',
            'item_id': item_id
        }), 201
    else:
        return jsonify({
            'error': 'Помилка при створенні товару'
        }), 500


if __name__ == '__main__':
    app.run(debug=True)