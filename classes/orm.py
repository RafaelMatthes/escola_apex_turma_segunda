import mysql.connector

from classes.student import Student
from classes.subject import Subject

class Connection():
    def __init__(self):
        try:
            self._db = mysql.connector.connect(
                host='localhost',
                database='apex_escola',
                user='admin',
                password='pass@1803'
            )
            self._cursor = self._db.cursor()
            print("Conectado !")


        except Exception as e:
            print(f"Erro ao conectar no bando de dados. error {e}")

class StudentsDataBase(Connection):

    def __init__(self):
        super().__init__()

        self._create_table()

    def _create_table(self):

        query = (
            "CREATE TABLE IF NOT EXISTS students ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "first_name VARCHAR(255) NOT NULL,"
            "last_name VARCHAR(255) NOT NULL,"
            "classroom VARCHAR(255) NOT NULL,"
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            ")  ENGINE=INNODB;"
        )
        self._cursor.execute(query)

    def insert(self, first_name, last_name, classroom):

        self._cursor.execute(
            f"INSERT INTO students (first_name, last_name, classroom) VALUES (%s,%s, %s)",
            (f"'{first_name}'", f"'{last_name}'", f"'{classroom}'")
        )

        self._db.commit()
        query = self.select(last=True)

        return query[len(query)-1]

    def select(self, last=True):

        if last:
            self._cursor.execute(f"SELECT * FROM students ORDER BY id DESC LIMIT 1;")
        else:
            self._cursor.execute("SELECT * FROM students")

        result = self._cursor.fetchall()

        return [ Student(
                first_name=student[1],
                last_name=student[2],
                classroom=student[3],
                id=student[0]
            )
            for student in result
        ]

class SubjectDataBase(Connection):

    def __init__(self):
        super().__init__()

        self._create_table()

    def _create_table(self):

        query = (
            "CREATE TABLE IF NOT EXISTS subject ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "name VARCHAR(255) NOT NULL,"
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            ")  ENGINE=INNODB;"
        )
        self._cursor.execute(query)

    def insert_if_not_exists(self, subject_name):

        subject = self.select(subject_name=subject_name)

        if not subject:
            print(f"INSERT INTO subject (name) VALUES ('{subject_name}')")

            self._cursor.execute(
                f"INSERT INTO subject (name) VALUES ('{subject_name}')"
            )

            self._db.commit()

            subject = self.select(subject_name=subject_name)

            print(subject)

        return subject

    def select(self, subject_name=None):

        if subject_name:

            self._cursor.execute(
                f"SELECT * FROM subject WHERE name = (%s)",
                (f"{subject_name}",)
            )
        else:
            self._cursor.execute("SELECT * FROM subject")

        result = self._cursor.fetchall()

        print(result)

        return [ Subject(
                id=subject[0],
                name=subject[1],
            )
            for subject in result
        ]

class GradeDataBase(Connection):

    def __init__(self):
        super().__init__()

        self._create_table()

    def _create_table(self):

        query = (
            "CREATE TABLE IF NOT EXISTS grade ("
            "id INT AUTO_INCREMENT PRIMARY KEY,"
            "student_id INT NOT NULL,"
            "subject_id INT NOT NULL,"
            "value VARCHAR(2) NOT NULL,"
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "FOREIGN KEY (student_id) REFERENCES students(id),"
            "FOREIGN KEY (subject_id) REFERENCES subject(id)"
            ")  ENGINE=INNODB;"
        )
        self._cursor.execute(query)

    def insert(self, student_id, subject_id, value):

        self._cursor.execute(
            f"INSERT INTO grade (student_id, subject_id, value) VALUES (%s,%s,%s)",
            (f"'{student_id}'",f"'{subject_id}'",f"{value}")
        )

        self._db.commit()

    def select(self, student_id, subject_id=None):

        query = f"SELECT * FROM subject WHERE student_id = {student_id}"

        if subject_id:
            query += f"subject_id = {subject_id}"

        self._cursor.execute(query)

        result = self._cursor.fetchall()

        pass