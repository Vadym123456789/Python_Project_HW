import string
import keyword
# Тестові приклади
test_cases = ['_', '___', 'x', 'get_value', 'get value', 'get!value', 'some_super_puper_value',
              'Get_value', 'get_Value', 'getValue', '3m', 'm3', 'assert', 'assert_exception']
for name in test_cases:
    # Перевірка зареєстрованих слів
    if name in keyword.kwlist:
        print(f"{name}: False")
        continue
    # Перевірка кількості підкреслень
    if name.count('_') > 1:
        print(f"{name}: False")
        continue
    # Перевірка, чи починається з цифри
    if name[0].isdigit():
        print(f"{name}: False")
        continue
    # Перевірка на великі літери, пробіли і недопустиму пунктуацію
    if any(char.isupper() or char.isspace() or (char in string.punctuation and char != '_') for char in name):
        print(f"{name}: False")
    else:
        print(f"{name}: True")







