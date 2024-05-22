import psycopg2
from contextlib import contextmanager
import logging
import random
from faker import Faker
from pathlib import Path

BASE_DIR = Path(__file__).parent
QUERIES = BASE_DIR / 'select_queries'

fake = Faker("en-GB")
subjects = ['Mathematic',
            'Physics',
            'Chemistry',
            'Biology',
            'History',
            'Geography',
            'Philosophy'
            ]


@contextmanager
def create_connection():
    try:
        conn = psycopg2.connect(host='localhost', database='university', user='postgres', password='5432')
        yield conn
        conn.close()
    except psycopg2.OperationalError as err:
        raise RuntimeError(f'Failed to create db {err}')


def create_db(sql_expression:str):
    conn = psycopg2.connect(host='localhost', database = 'postgres', user = 'postgres', password = '5432')
    conn.autocommit = True
    c = conn.cursor()
    c.execute(sql_expression)
    print("Database created successfully")
    conn.commit()
    c.close()

if __name__ == '__main__':
    sql_create_db = """CREATE database university;"""

    sql_insert_into_groups_table = ("INSERT INTO groups (name) VALUES (%s)")
    sql_insert_into_teachers_table = ("INSERT INTO teachers (name) VALUES (%s)")
    sql_insert_into_subjects_table = ("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s)")
    sql_insert_into_students_table = ("INSERT INTO students (name, group_id) VALUES (%s, %s) RETURNING id")
    sql_insert_into_grades_table = ("INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s)")

    try:
        create_db(sql_create_db)
        with create_connection() as conn:
            if conn is not None:
                with conn.cursor() as cursor:
                    cursor.execute(open('insert.sql', 'r').read())
                    print("Tables created successfully")
                    for i in range(1, 4):
                        group_data = (f'group{i}',)
                        cursor.execute(sql_insert_into_groups_table, group_data)
                    for i in range(1, 8):
                        teacher_name = (fake.name(),)
                        cursor.execute(sql_insert_into_teachers_table, teacher_name)   
                    for teacher_id in range(1, 8):
                        subject_name = subjects[teacher_id-1]
                        cursor.execute(sql_insert_into_subjects_table, (subject_name, teacher_id))
                    for group_id in range(1, 4):
                        for _ in range(1, random.randint(35, 40)):
                            cursor.execute(sql_insert_into_students_table, (fake.name(), group_id))
                            student_id = cursor.fetchone()[0]
                            for subject_id in range(1, 8):
                                for _ in range(3):
                                    cursor.execute(sql_insert_into_grades_table, (student_id, subject_id, random.randint(1, 100), fake.date_between(start_date = '-3M', end_date = 'today')))
                    print("Data inserted into tables successfully")
                    for file in QUERIES.iterdir():       
                        with open(QUERIES / file, 'r') as f:
                            print('\n' + f.readline().strip('\n'))
                            query = f.read()
                            cursor.execute(query)
                            for item in cursor.fetchall():
                                print(item)
                                #print(''.join(['' + str(el) + ' | ' for el in item]))
                    conn.commit()
            else:
                print("Error! cannot create the database connection.")
    except RuntimeError as err:
        logging.error(err)