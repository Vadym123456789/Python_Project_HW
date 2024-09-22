import random

# Створення випадкового списку
number_of_elements = random.randint(3, 10)
original_list = [random.randint(1, 100) for _ in range(number_of_elements)]

# Створення нового списку з потрібних елементів
result_list = [original_list[0], original_list[2], original_list[-2]]

# Виведення результатів
print(f"Оригінальний список: {original_list}")
print(f"Результуючий список: {result_list}")