import string
import keyword

# Отримання вводу від користувача
user_input = input("Введіть ім'я змінної: ")

# Ініціалізація результату
is_valid = True

# Перевірка на пустий рядок
if not user_input:
    is_valid = False

# Перевірка на початок з цифри
elif user_input[0].isdigit():
    is_valid = False

# Перевірка на наявність великих літер
elif any(char.isupper() for char in user_input):
    is_valid = False

# Перевірка на наявність пробілів та знаків пунктуації (крім _)
elif any(char not in string.ascii_lowercase + string.digits + '_' for char in user_input):
    is_valid = False

# Перевірка на кількість нижніх підкреслень
elif user_input.count('_') > 1:
    is_valid = False

# Перевірка на зареєстровані слова
elif user_input in keyword.kwlist:
    is_valid = False

# Виведення результату
print(is_valid)