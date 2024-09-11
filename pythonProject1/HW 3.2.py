def move_last_to_first(lst):
    if len(lst) <= 1:
        return lst
    return [lst[-1]] + lst[:-1]

# Тестові приклади
test_cases = [
    [12, 3, 4, 10],
    [1],
    [],
    [12, 3, 4, 10, 8]
]

# Перевірка кожного тестового випадку
for case in test_cases:
    result = move_last_to_first(case)
    print(f"{case} => {result}")