
number = int(input("Введіть 5-значне число: "))

# Розділяємо число на окремі цифри
fifth = number % 10
fourth = (number // 10) % 10
third = (number // 100) % 10
second = (number // 1000) % 10
first = number // 10000

# Збираємо число у зворотньому порядку
reversed_number = fifth * 10000 + fourth * 1000 + third * 100 + second * 10 + first

# Виводимо результат
print(reversed_number)