import mysql.connector

from student import Student

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

    def select(self, name=None):

        if name:
            self._cursor.execute(f"SELECT * FROM students WHERE name = {name}")
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