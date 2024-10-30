# student.py
class Student:
    def __init__(self, gender, age, name, surname, record_book):
        self.gender = gender
        self.age = age
        self.name = name
        self.surname = surname
        self.record_book = record_book

    def __str__(self):
        return f"{self.name} {self.surname}"

    def __eq__(self, other):
        if isinstance(other, Student):
            return str(self) == str(other)
        return False

    def __hash__(self):
        return hash(str(self))


# group.py
class Group:
    def __init__(self, name):
        self.name = name
        self.group = set()

    def add_student(self, student):
        self.group.add(student)

    def delete_student(self, surname):
        student_to_remove = self.find_student(surname)
        if student_to_remove:
            self.group.remove(student_to_remove)

    def find_student(self, surname):
        for student in self.group:
            if student.surname == surname:
                return student
        return None

    def __str__(self):
        all_students = "\n".join(str(student) for student in self.group)
        return f"Group: {self.name}\n{all_students}"


# main.py
from student import Student
from group import Group


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
    print(gr)

    # Перевіряємо пошук студента
    assert gr.find_student('Jobs') == st1  # Повинно знайти Steve Jobs
    assert gr.find_student('Jobs2') is None  # Повинно повернути None

    # Видаляємо студента
    gr.delete_student('Taylor')

    # Виводимо оновлений стан групи
    print(gr)  # Повинен залишитися тільки один студент


if __name__ == "__main__":
    main()