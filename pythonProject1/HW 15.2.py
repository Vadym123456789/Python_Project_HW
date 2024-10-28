class Fraction:
    def __init__(self, a, b):
        # Перевіряємо, щоб знаменник не був нулем
        if b == 0:
            raise ValueError("Знаменник не може бути нулем")
        self.a = a  # Чисельник
        self.b = b  # Знаменник

    def get_common_denominator(self, other):
        """Допоміжний метод для отримання спільного знаменника"""
        return self.b * other.b

    def __mul__(self, other):
        """Множення дробів"""
        new_a = self.a * other.a
        new_b = self.b * other.b
        return Fraction(new_a, new_b)

    def __add__(self, other):
        """Додавання дробів"""
        # Знаходимо спільний знаменник
        common_b = self.get_common_denominator(other)
        # Розраховуємо нові чисельники
        new_a1 = self.a * (common_b // self.b)
        new_a2 = other.a * (common_b // other.b)
        # Додаємо чисельники
        return Fraction(new_a1 + new_a2, common_b)

    def __sub__(self, other):
        """Віднімання дробів"""
        # Знаходимо спільний знаменник
        common_b = self.get_common_denominator(other)
        # Розраховуємо нові чисельники
        new_a1 = self.a * (common_b // self.b)
        new_a2 = other.a * (common_b // other.b)
        # Віднімаємо чисельники
        return Fraction(new_a1 - new_a2, common_b)

    def get_decimal(self):
        """Допоміжний метод для порівняння - переводить дріб у десяткове число"""
        return self.a / self.b

    def __eq__(self, other):
        """Перевірка на рівність"""
        return self.get_decimal() == other.get_decimal()

    def __gt__(self, other):
        """Перевірка чи поточний дріб більший за інший"""
        return self.get_decimal() > other.get_decimal()

    def __lt__(self, other):
        """Перевірка чи поточний дріб менший за інший"""
        return self.get_decimal() < other.get_decimal()

    def __str__(self):
        return f"Fraction: {self.a}, {self.b}"


# Тестування
f_a = Fraction(2, 3)
f_b = Fraction(3, 6)
f_c = f_b + f_a
assert str(f_c) == 'Fraction: 21, 18'  # 2/3 + 3/6 = 12/18 + 9/18 = 21/18

f_d = f_b * f_a
assert str(f_d) == 'Fraction: 6, 18'  # 2/3 * 3/6 = 6/18

f_e = f_a - f_b
assert str(f_e) == 'Fraction: 3, 18'  # 2/3 - 3/6 = 12/18 - 9/18 = 3/18

assert f_d < f_c  # 6/18 < 21/18
assert f_d > f_e  # 6/18 > 3/18
assert f_a != f_b  # 2/3 ≠ 3/6

f_1 = Fraction(2, 4)
f_2 = Fraction(3, 6)
assert f_1 == f_2  # 2/4 = 3/6 = 1/2

print('OK')