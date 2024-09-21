# Тестові випадки
test_cases = [
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3],
    [1, 2, 3, 4, 5],
    [1],
    []
]

# Обробка кожного тестового випадку
for lst in test_cases:
    if not lst:
        result = [[], []]
    else:
        mid = len(lst) // 2
        if len(lst) % 2 != 0:
            mid += 1
        result = [lst[:mid], lst[mid:]]

    print(f"{lst} => {result}")

# Перевірка кожного тестового випадку
for case in test_cases:
    result = split_list(case)
    print(f"{case} => {result}")