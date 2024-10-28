def __add__(self, other):
    new_square = self.get_square() + other.get_square()
    # Зберігаємо пропорції першого прямокутника
    ratio = self.width / self.height
    new_height = (new_square / ratio) ** 0.5
    new_width = new_square / new_height
    return Rectangle(new_width, new_height)

def __mul__(self, n):
    new_square = self.get_square() * n
    # Зберігаємо пропорції
    ratio = self.width / self.height
    new_height = (new_square / ratio) ** 0.5
    new_width = new_square / new_height
    return Rectangle(new_width, new_height)