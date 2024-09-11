def split_list(lst):
    if not lst:
        return [[], []]

    mid = (len(lst) + 1) // 2
    return [lst[:mid], lst[mid:]]


# Тестові випадки
test_cases = [
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3],
    [1, 2, 3, 4, 5],
    [1],
    []
]

# Перевірка кожного тестового випадку
for case in test_cases:
    result = split_list(case)
    print(f"{case} => {result}")