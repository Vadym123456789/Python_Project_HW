# Тестові приклади
test_cases = [
    [0, 1, 0, 12, 3],
    [0],
    [1, 0, 13, 0, 0, 0, 5],
    [9, 0, 7, 31, 0, 45, 0, 45, 0, 45, 0, 0, 96, 0]
]

# Обробка кожного тестового випадку
for original_list in test_cases:
    # Створюємо новий список для ненульових елементів
    non_zero = []
    # Підраховуємо кількість нулів
    zero_count = 0

    # Проходимо по всіх елементах вхідного списку
    for num in original_list:
        if num != 0:
            non_zero.append(num)
        else:
            zero_count += 1

    # Додаємо нулі в кінець списку
    result = non_zero + [0] * zero_count

    # Виводимо результат
    print(f"{original_list} -> {result}")