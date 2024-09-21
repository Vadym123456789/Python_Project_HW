# Тестові випадки
test_cases = [
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3],
    [1, 2, 3, 4, 5],
    [1],
    []
]

# Обробка кожного тестового випадку
for input_list in test_cases:
    # Обчислення індексу середини списку
    mid = len(input_list) // 2

    # Розділення списку на дві частини
    first_half = input_list[:mid]
    second_half = input_list[mid:]

    # Формування результату
    result = [first_half, second_half]

    # Виведення результату
    print(f"{input_list} => {result}")