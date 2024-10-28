from flask import Flask, request

# Створюємо екземпляр Flask застосунку
app = Flask(__name__)

# Авторизація та реєстрація
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'Отримання форми логіну'
    if request.method == 'POST':
        return 'Обробка даних логіну'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return 'Отримання форми реєстрації'
    if request.method == 'POST':
        return 'Обробка даних реєстрації'

@app.route('/logout', methods=['POST'])
def logout():
    return 'Вихід з системи'

# Профіль користувача
@app.route('/profile', methods=['GET', 'PUT', 'DELETE'])
def profile():
    if request.method == 'GET':
        return 'Отримання даних профілю'
    if request.method == 'PUT':
        return 'Оновлення даних профілю'
    if request.method == 'DELETE':
        return 'Видалення профілю'

@app.route('/profile/favorites', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def favorites():
    if request.method == 'GET':
        return 'Отримання списку обраного'
    if request.method == 'POST':
        return 'Додавання в обране'
    if request.method == 'PATCH':
        return 'Оновлення даних обраного'
    if request.method == 'DELETE':
        return 'Очищення всього списку обраного'

@app.route('/profile/favorites/<favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    return f'Видалення конкретного обраного {favorite_id}'

@app.route('/profile/search_history', methods=['GET', 'DELETE'])
def search_history():
    if request.method == 'GET':
        return 'Отримання історії пошуку'
    if request.method == 'DELETE':
        return 'Очищення історії пошуку'

# Робота з items
@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        return 'Отримання списку items'
    if request.method == 'POST':
        return 'Створення нового item'

@app.route('/items/<item_id>', methods=['GET', 'DELETE'])
def item(item_id):
    if request.method == 'GET':
        return f'Отримання інформації про item {item_id}'
    if request.method == 'DELETE':
        return f'Видалення item {item_id}'

# Робота з leasers
@app.route('/leasers', methods=['GET'])
def leasers():
    return 'Отримання списку орендодавців'

@app.route('/leasers/<leaser_id>', methods=['GET'])
def leaser(leaser_id):
    return f'Отримання інформації про орендодавця {leaser_id}'

# Робота з контрактами
@app.route('/contracts', methods=['GET', 'POST'])
def contracts():
    if request.method == 'GET':
        return 'Отримання списку контрактів'
    if request.method == 'POST':
        return 'Створення нового контракту'

@app.route('/contracts/<contract_id>', methods=['GET', 'PATCH'])
def contract(contract_id):
    if request.method == 'GET':
        return f'Отримання інформації про контракт {contract_id}'
    if request.method == 'PATCH':
        return f'Оновлення даних контракту {contract_id}'

# Пошук
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return 'Пошук за GET параметрами'
    if request.method == 'POST':
        return 'Пошук з розширеними параметрами через POST'

# Додаткові функції
@app.route('/complain', methods=['POST'])
def complain():
    return 'Створення скарги'

@app.route('/compare', methods=['GET', 'PATCH'])
def compare():
    if request.method == 'GET':
        return 'Отримання списку порівняння'
    if request.method == 'PATCH':
        return 'Оновлення списку порівняння'

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)