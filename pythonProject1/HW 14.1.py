class Human:
    def __init__(self, gender, age, first_name, last_name):
        self.gender = gender
        self.age = age
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}, Gender: {self.gender}, Age: {self.age}"


class Student(Human):
    def __init__(self, gender, age, first_name, last_name, record_book):
        super().__init__(gender, age, first_name, last_name)
        self.record_book = record_book

    def __str__(self):
        return f"{super().__str__()}, Record Book: {self.record_book}"


class GroupLimitError(Exception):
    """Виняток, що викидається при перевищенні ліміту студентів у групі"""

    def __init__(self, message="Перевищено максимальну кількість студентів у групі (10)"):
        self.message = message
        super().__init__(self.message)


class Group:
    MAX_STUDENTS = 10

    def __init__(self, number):
        self.number = number
        self.group = set()

    def add_student(self, student):
        if len(self.group) >= self.MAX_STUDENTS:
            raise GroupLimitError()
        self.group.add(student)

    def find_student(self, last_name):
        for student in self.group:
            if student.last_name == last_name:
                return student
        return None

    def delete_student(self, last_name):
        student = self.find_student(last_name)
        if student:
            self.group.remove(student)

    def __str__(self):
        all_students = '\n'.join(str(student) for student in self.group)
        return f'Number: {self.number}\n{all_students}'


# Тестування
if __name__ == "__main__":
    # Створюємо групу
    group = Group('PD1')

    # Створюємо 11 студентів
    students = [
        Student('Male', 20, f'Name{i}', f'Lastname{i}', f'AN{i}')
        for i in range(1, 12)
    ]

    # Додаємо студентів та обробляємо виняток
    for student in students:
        try:
            print(f"Спроба додати студента {student.first_name} {student.last_name}")
            group.add_student(student)
            print("Студента успішно додано")
        except GroupLimitError as e:
            print(f"Помилка: {e}")
            break

    print("\nПоточний склад групи:")
    print(group)
    print(f"\nКількість студентів у групі: {len(group.group)}")

    # Додаткове тестування інших методів
    print("\nТестування пошуку:")
    found_student = group.find_student('Lastname1')
    if found_student:
        print(f"Знайдено студента: {found_student}")

    print("\nВидалення студента:")
    group.delete_student('Lastname1')
    print(f"Кількість студентів після видалення: {len(group.group)}")

    print("\nСпроба додати ще одного студента після видалення:")
    try:
        new_student = Student('Female', 19, 'New', 'Student', 'AN999')
        group.add_student(new_student)
        print("Студента успішно додано")
    except GroupLimitError as e:
        print(f"Помилка: {e}")