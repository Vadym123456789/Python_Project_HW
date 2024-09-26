import string

# Отримуємо ввід від користувача
user_input = input("Введіть дві літери через дефіс (наприклад, 'a-c'): ")

# Розділяємо ввід на початкову та кінцеву літери
start, end = user_input.split('-')

# Знаходимо індекси початкової та кінцевої літер в string.ascii_letters
start_index = string.ascii_letters.index(start)
end_index = string.ascii_letters.index(end)

# Створюємо підрядок з літерами між start та end (включно)
result = string.ascii_letters[start_index:end_index+1]

# Виводимо результат
print(result)