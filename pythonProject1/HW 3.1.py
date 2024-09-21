# Введення чисел та операції від користувача
num1 = float(input("Введіть перше число: "))
num2 = float(input("Введіть друге число: "))
operation = input("Введіть операцію (+, -, *, /): ")

# Виконання математичної операції
if operation == '+':
    result = num1 + num2
    print(f"Результат: {result}")
elif operation == '-':
    result = num1 - num2
    print(f"Результат: {result}")
elif operation == '*':
    result = num1 * num2
    print(f"Результат: {result}")
elif operation == '/':
    if num2 != 0:
        result = num1 / num2
        print(f"Результат: {result}")
    else:
        print("Помилка: Ділення на нуль!")
else:
    print("Помилка: Невідома операція!")

# Основна програма
print("Простий калькулятор")
num1 = float(input("Введіть перше число: "))
num2 = float(input("Введіть друге число: "))
operation = input("Введіть операцію (+, -, *, /): ")

result = calculate(num1, num2, operation)
print(f"Результат: {result}")