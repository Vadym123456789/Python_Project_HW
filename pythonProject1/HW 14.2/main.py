import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.student import Student
from models.group import Group


def main():
    # Створюємо студентів
    st1 = Student('Male', 30, 'Steve', 'Jobs', 'AN142')
    st2 = Student('Female', 25, 'Liza', 'Taylor', 'AN145')

    # Створюємо групу
    gr = Group('PD1')

    # Додаємо студентів
    gr.add_student(st1)
    gr.add_student(st2)

    # Виводимо початковий стан групи
    print("Початковий стан групи:")
    print(gr)

    # Перевіряємо пошук студентів
    assert gr.find_student('Jobs') == st1
    assert gr.find_student('Jobs2') is None

    # Видаляємо студента
    print("\nВидаляємо студента Taylor")
    gr.delete_student('Taylor')

    # Виводимо кінцевий стан групи
    print("\nКінцевий стан групи:")
    print(gr)


if __name__ == "__main__":
    main()