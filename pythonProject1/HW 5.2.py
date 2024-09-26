while True:
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

    # Запит на продовження роботи
    continue_calc = input("Бажаєте продовжити? (y/yes для продовження): ").lower()
    if continue_calc != 'y' and continue_calc != 'yes':
        break

print("Дякуємо за використання калькулятора!")