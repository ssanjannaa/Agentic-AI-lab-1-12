"""
Database Seeder for University Database AI Assistant
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)

Populates data/university.db with synthetic academic data.
"""

import os
import sqlite3

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATA_DIR, "university.db")

def init_db(db_path: str = DB_PATH) -> str:
    """Initializes SQLite database schema and seeds sample records."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Remove existing db file if recreating
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Departments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        code TEXT NOT NULL UNIQUE
    );
    """)

    # 2. Students Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_number TEXT NOT NULL UNIQUE,
        department_id INTEGER NOT NULL,
        semester INTEGER NOT NULL,
        cgpa REAL NOT NULL,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    );
    """)

    # 3. Courses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT NOT NULL UNIQUE,
        course_name TEXT NOT NULL,
        department_id INTEGER NOT NULL,
        credits INTEGER NOT NULL,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    );
    """)

    # 4. Enrollments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    );
    """)

    # 5. Faculty Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department_id INTEGER NOT NULL,
        designation TEXT NOT NULL,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    );
    """)

    # Seed Data Insertion
    departments_data = [
        (1, "Computer Science", "CS"),
        (2, "Cyber Security", "CSEC"),
        (3, "Artificial Intelligence", "AI"),
        (4, "Data Science", "DS"),
        (5, "Information Technology", "IT")
    ]
    cursor.executemany("INSERT INTO departments (id, name, code) VALUES (?, ?, ?);", departments_data)

    students_data = [
        ("Aarav Sharma", "23CS001", 1, 6, 9.4),
        ("Ananya Patel", "23CS002", 1, 6, 8.8),
        ("Rohan Verma", "23CS003", 1, 4, 7.9),
        ("Priya Nair", "23CS004", 1, 4, 9.6),
        ("Vikram Singh", "23CS005", 1, 6, 8.1),
        ("Neha Gupta", "23CSEC001", 2, 6, 9.1),
        ("Karan Mehta", "23CSEC002", 2, 4, 8.4),
        ("Diya Reddy", "23CSEC003", 2, 6, 8.9),
        ("Aditya Kumar", "23CSEC004", 2, 4, 7.5),
        ("Siddharth Joshi", "23AI001", 3, 6, 9.8),
        ("Kavya Deshmukh", "23AI002", 3, 6, 9.2),
        ("Rahul Rao", "23AI003", 3, 4, 8.6),
        ("Ishita Saxena", "23AI004", 3, 4, 8.3),
        ("Arjun Roy", "23DS001", 4, 6, 8.7),
        ("Tanvi Bhat", "23DS002", 4, 4, 9.0),
        ("Manish Iyer", "23DS003", 4, 6, 7.8),
        ("Riya Pillai", "23IT001", 5, 6, 8.5),
        ("Varun Agarwal", "23IT002", 5, 4, 8.2),
        ("Simran Kaur", "23IT003", 5, 6, 9.3),
        ("Devendra Dave", "23IT004", 5, 4, 7.6)
    ]
    cursor.executemany("INSERT INTO students (name, roll_number, department_id, semester, cgpa) VALUES (?, ?, ?, ?, ?);", students_data)

    courses_data = [
        ("CS101", "Data Structures & Algorithms", 1, 4),
        ("CS201", "Database Management Systems", 1, 4),
        ("CS301", "Operating Systems", 1, 3),
        ("CSEC101", "Network Security Fundamentals", 2, 4),
        ("CSEC201", "Applied Cryptography", 2, 3),
        ("CSEC301", "Ethical Hacking & Penetration Testing", 2, 4),
        ("AI101", "Artificial Intelligence Foundations", 3, 4),
        ("AI201", "Machine Learning Algorithms", 3, 4),
        ("AI301", "Deep Learning & Neural Networks", 3, 4),
        ("DS101", "Data Mining & Data Warehousing", 4, 3),
        ("DS201", "Big Data Analytics", 4, 4),
        ("IT101", "Web Engineering & APIs", 5, 3)
    ]
    cursor.executemany("INSERT INTO courses (course_code, course_name, department_id, credits) VALUES (?, ?, ?, ?);", courses_data)

    enrollments_data = [
        (1, 1, "A+"), (1, 2, "A"), (2, 1, "A"), (2, 2, "B+"),
        (3, 1, "B"), (3, 2, "B+"), (4, 1, "A+"), (4, 3, "A"),
        (5, 2, "B+"), (6, 4, "A+"), (6, 5, "A"), (7, 4, "B+"),
        (8, 5, "A"), (8, 6, "A+"), (9, 4, "B"), (10, 7, "A+"),
        (10, 8, "A+"), (10, 9, "A+"), (11, 7, "A"), (11, 8, "A"),
        (12, 7, "B+"), (12, 8, "A"), (13, 7, "B"), (14, 10, "A"),
        (14, 11, "B+"), (15, 10, "A+"), (15, 11, "A"), (16, 10, "B"),
        (17, 12, "A"), (18, 12, "B+"), (19, 12, "A+"), (20, 12, "C")
    ]
    cursor.executemany("INSERT INTO enrollments (student_id, course_id, grade) VALUES (?, ?, ?);", enrollments_data)

    faculty_data = [
        ("Dr. Rajesh Kulkarni", 1, "Professor & HOD"),
        ("Prof. Sunita Menon", 1, "Associate Professor"),
        ("Dr. Amitav Ghosh", 2, "Professor & HOD"),
        ("Prof. Meera Sen", 2, "Assistant Professor"),
        ("Dr. Vikramaditya Sen", 3, "Professor & HOD"),
        ("Dr. Shalini Prasad", 3, "Associate Professor"),
        ("Dr. Sumeet Hegde", 4, "Professor & HOD"),
        ("Prof. Anupama Nair", 4, "Assistant Professor"),
        ("Dr. Ramesh Chandra", 5, "Professor & HOD"),
        ("Prof. Pooja Sundaram", 5, "Assistant Professor")
    ]
    cursor.executemany("INSERT INTO faculty (name, department_id, designation) VALUES (?, ?, ?);", faculty_data)

    conn.commit()
    conn.close()
    print(f"[OK] Successfully seeded database at: {db_path}")
    return db_path

if __name__ == "__main__":
    init_db()
