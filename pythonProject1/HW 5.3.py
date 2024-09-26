import string

# Отримуємо вхідний рядок від користувача
input_string = input("Введіть рядок для перетворення на хештег: ")

# Видаляємо знаки пунктуації та розділяємо рядок на слова
words = input_string.split()
clean_words = []
for word in words:
    clean_word = ''.join(char for char in word if char not in string.punctuation)
    if clean_word:
        clean_words.append(clean_word)

# Перетворюємо кожне слово так, щоб воно починалося з великої літери
capitalized_words = [word.capitalize() for word in clean_words]

# Об'єднуємо слова в один рядок
hashtag = ''.join(capitalized_words)

# Додаємо символ # на початок
hashtag = '#' + hashtag

# Обрізаємо хештег до 140 символів, якщо він довший
if len(hashtag) > 140:
    hashtag = hashtag[:140]

# Виводимо результат
print(hashtag)