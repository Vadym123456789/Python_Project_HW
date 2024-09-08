# Просимо користувача ввести 4-значне число
number = int(input("Введіть 4-значне число: "))

# Отримуємо цифри числа за допомогою операцій ділення
thousands = number // 1000
hundreds = (number % 1000) // 100
tens = (number % 100) // 10
ones = number % 10

# Виводимо цифри в стовпчик
print(thousands)
print(hundreds)
print(tens)
print(ones)