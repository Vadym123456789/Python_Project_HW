test_cases = [
    [12, 3, 4, 10],
    [1],
    [],
    [12, 3, 4, 10, 8]
]

# Перевірка кожного тестового випадку
for lst in test_cases:
    if len(lst) <= 1:
        result = lst
    else:
        result = [lst[-1]] + lst[:-1]
    print(f"{lst} => {result}")