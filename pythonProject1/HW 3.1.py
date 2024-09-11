# Функція для виконання математичних операцій
def calculate(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 != 0:
            return num1 / num2
        else:
            return "Помилка: Ділення на нуль!"
    else:
        return "Помилка: Невідома операція!"

# Основна програма
print("Простий калькулятор")
num1 = float(input("Введіть перше число: "))
num2 = float(input("Введіть друге число: "))
operation = input("Введіть операцію (+, -, *, /): ")

result = calculate(num1, num2, operation)
print(f"Результат: {result}")