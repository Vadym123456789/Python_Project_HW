# Отримуємо ввід від користувача
number = input("Введіть ціле число: ")

# Цикл продовжується, поки число більше 9
while int(number) > 9:
    result = 1

    # Перемножуємо всі цифри числа
    for digit in number:
        result *= int(digit)

    # Оновлюємо number для наступної ітерації
    number = str(result)

# Виводимо результат
print(number)