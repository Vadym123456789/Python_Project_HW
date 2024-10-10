def popular_words(text, words):
    # Перетворюємо весь текст у нижній регістр і розбиваємо на окремі слова
    text = text.lower().split()
    # Створюємо словник для результатів
    result = {}
    # Для кожного слова з списку words рахуємо його кількість у тексті
    for word in words:
        result[word] = text.count(word)
    return result
# Перевірка
assert popular_words('''When I was One I had just begun
When I was Two I was nearly new''', ['i', 'was', 'three', 'near']) == {
    'i': 4,
    'was': 3,
    'three': 0,
    'near': 0
}, 'Test1'
print('OK')









