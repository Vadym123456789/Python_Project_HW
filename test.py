# Імпортуємо необхідні модулі з Flask
from flask import Flask, request

# Створюємо екземпляр Flask-додатку
app = Flask(__name__)

"""
Опис всіх маршрутів API:
/login [GET, POST]
/register [GET, POST]
/logout [GET ? POST ?? DELETE]

/profile (/user, /me) [GET, PUT(PATCH), DELETE]
      ?  /favouties [GET, POST, DELETE, PATCH]
      ??  /favouties/<favourite_id> [DELETE]
      ?  /search_history [GET, DELETE]

/items [GET, POST]
/items/<item_id> [GET, DELETE]
/leasers [GET]
/leasers/<leaser_id> [GET]

/contracts [GET, POST]
/contracts/<contract_id> [GET, PATCH/PUT]

/search [GET, (POST)]

/complain [POST]
/compare [GET, PUT/PATCH]
"""

# Визначаємо маршрут для головної сторінки '/'
@app.route('/')  # Декоратор, який вказує URL для цієї функції
def home():      # Функція, яка буде виконана при переході на URL '/'
    return 'Hello World!'  # Повертає відповідь, яку побачить користувач

# Визначаємо маршрут для сторінки логіну
@app.route('/login', methods=['GET', 'POST'])  # Вказуємо, що цей маршрут приймає GET та POST запити
def login():
    # Перевіряємо, який тип запиту був отриманий
    if request.method == 'GET':
        return 'Це GET запит на сторінку логіну'  # Повертається при GET запиті
    if request.method == 'POST':
        return 'Це POST запит на сторінку логіну'  # Повертається при POST запиті

# Перевіряємо, чи файл запущено напряму (не імпортовано як модуль)
if __name__ == '__main__':
    # Запускаємо веб-сервер з увімкненим режимом налагодження
    app.run(debug=True)