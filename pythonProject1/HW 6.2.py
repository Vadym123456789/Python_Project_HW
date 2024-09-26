# Отримуємо ввід від користувача
seconds = int(input("Введіть кількість секунд (0-8639999): "))
# Перевірка введеного значення
if seconds < 0 or seconds > 8639999:
    print("Неправильне значення. Введіть число від 0 до 8639999.")
else:
    # Розрахунок днів, годин, хвилин та секунд
    days, remainder = divmod(seconds, 86400)  # 86400 секунд у добі
    hours, remainder = divmod(remainder, 3600)  # 3600 секунд у годині
    minutes, seconds = divmod(remainder, 60)  # 60 секунд у хвилині
    # Визначення правильної форми слова "день" без використання функції
    if 11 <= days % 100 <= 19:
        day_word = "днів"
    elif days % 10 == 1:
        day_word = "день"
    elif 2 <= days % 10 <= 4:
        day_word = "дні"
    else:
        day_word = "днів"
    # Форматування результату
    result = f"{days} {day_word}, {str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
    # Виведення результату
    print(result)







