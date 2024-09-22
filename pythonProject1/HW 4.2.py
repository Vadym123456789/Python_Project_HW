# Тестові приклади
test_cases = [
    [0, 1, 7, 2, 4, 8],
    [1, 3, 5],
    [6],
    []
]

# Обробка кожного тестового випадку
for numbers in test_cases:
    if not numbers:
        result = 0
    else:
        # Сума елементів з парними індексами
        sum_even_indices = sum(numbers[0::2])

        # Множення суми на останній елемент
        result = sum_even_indices * numbers[-1]

    print(f"{numbers} => {result}")