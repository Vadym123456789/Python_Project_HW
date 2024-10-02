def common_elements():
    list_1 = {x for x in range(100) if x % 3 == 0}
    list_2 = {x for x in range(100) if x % 5 == 0}
    common_set = list_1 & list_2  # Перетин множин
    return common_set
# Перевірка
assert common_elements() == {0, 75, 45, 15, 90, 60, 30}