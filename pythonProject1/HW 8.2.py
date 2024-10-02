import re


def is_palindrome(text):
    # Видаляємо всі символи, крім букв та цифр, і переводимо в нижній регістр
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text.lower())

    # Порівнюємо очищений текст з його реверсом
    return cleaned_text == cleaned_text[::-1]


assert is_palindrome('A man, a plan, a canal: Panama') == True, 'Test1'
assert is_palindrome('0P') == False, 'Test2'
assert is_palindrome('a.') == True, 'Test3'
assert is_palindrome('aurora') == False, 'Test4'
print("ОК")