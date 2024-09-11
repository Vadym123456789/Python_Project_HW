# Просимо користувача ввести 4-значне число
number = int(input("Введіть 4-значне число: "))

# Отримуємо цифри числа за допомогою операцій ділення
thousands, remainder = divmod(number, 1000)
hundreds, remainder = divmod(remainder, 100)
tens, ones = divmod(remainder, 10)

# Виводимо цифри в стовпчик
print(thousands)
print(hundreds)
print(tens)
print(ones)