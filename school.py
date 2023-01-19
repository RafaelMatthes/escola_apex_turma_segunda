from classes.orm import StudentsDataBase, SubjectDataBase, GradeDataBase

class School():

    def __init__(self):
        self._student_database = StudentsDataBase()
        self._subject_database = SubjectDataBase()
        self._grade_database = GradeDataBase()

    def get_students(self):
        return self._student_database.select()

    def get_student_by_name(self, name):
        return self._student_database.select(name=name)

    def insert_student(self, first_name, last_name, classroom):
        return self._student_database.insert(
            first_name=first_name,
            last_name=last_name,
            classroom=classroom
        )

    def insert_grades(self, student_id, subject_id, value):
        self._grade_database.insert(student_id, subject_id, value)

    def add_grades_to_subject(self, student, subject):
        cont = True

        while cont:
            value = input("Informe a nota: ")

            self.insert_grades(
                student_id=student.id,
                subject_id=subject.id,
                value=value
            )

            cont = (
                input("deseja cadastrar outra nota? 'S' para continuar").upper() == 'S'
            )

    def insert_subject(self, subject_name):
        return self._subject_database.insert_if_not_exists(subject_name=subject_name)

    def add_subject_to_student(self, student):
        cont = True

        while cont:
            subject_name = input("Informe o nome da matéria: ")

            subject = self.insert_subject(
                subject_name=subject_name,
            )

            self.add_grades_to_subject(student, subject)

            cont = (
                input("deseja cadastrar outra matéria? 'S' para continuar").upper() == 'S'
            )

    def subscribe_students(self):
        cont = True

        while cont:
            first_name = input("Informe o primeiro nome do aluno: ")
            last_name = input("Informe o sobrenome do aluno: ")
            classroom = input("Informe o classe do aluno: ")

            student = self.insert_student(
                first_name=first_name,
                last_name=last_name,
                classroom=classroom
            )

            print(student.id)

            self.add_subject_to_student(student)

            cont = (
                input("deseja cadastrar outro aluno ? 'S' para continuar").upper() == 'S'
            )

apex = School()
apex.subscribe_students()
list = apex.get_students()

for student in list:
    print(student)