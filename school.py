from orm import StudentsDataBase

class School():

    def __init__(self):
        self._student_database = StudentsDataBase()

    def get_students(self):
        return self._student_database.select()

    def get_student_by_name(self, name):
        return self._student_database.select(name=name)

    def insert_student(self, first_name, last_name, classroom):
        self._student_database.insert(
            first_name=first_name,
            last_name=last_name,
            classroom=classroom
        )

    def subscribe_students(self):
        cont = True

        while cont:
            first_name = input("Informe o primeiro nome do aluno: ")
            last_name = input("Informe o sobrenome do aluno: ")
            classroom = input("Informe o classe do aluno: ")

            self.insert_student(
               first_name=first_name,
                last_name=last_name,
                classroom=classroom
            )

            cont = (
                input("deseja cadastrar outro aluno ? 'S' para continuar").upper() == 'S'
            )

apex = School()
apex.subscribe_students()
list = apex.get_students()

for student in list:
    print(student)