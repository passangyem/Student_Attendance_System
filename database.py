import sqlite3

DB_NAME = "attendance.db"


def connect():
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                academic_year TEXT NOT NULL,
                gender TEXT NOT NULL
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                UNIQUE(student_id, date),
                FOREIGN KEY(student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE
            )
        """)


# STUDENT FUNCTIONS

def add_student(student_id, name, year, gender):
    with connect() as con:
        con.execute("""
            INSERT INTO students
            (student_id, name, academic_year, gender)
            VALUES (?, ?, ?, ?)
        """, (student_id, name, year, gender))


def update_student(student_id, name, year, gender):
    with connect() as con:
        con.execute("""
            UPDATE students
            SET name=?, academic_year=?, gender=?
            WHERE student_id=?
        """, (name, year, gender, student_id))


def delete_student(student_id):
    with connect() as con:
        con.execute(
            "DELETE FROM students WHERE student_id=?",
            (student_id,)
        )


def get_students():
    with connect() as con:
        return con.execute("""
            SELECT student_id, name, academic_year, gender
            FROM students
            ORDER BY name
        """).fetchall()


def search_students(keyword):
    with connect() as con:
        return con.execute("""
            SELECT student_id, name, academic_year, gender
            FROM students
            WHERE student_id LIKE ? OR name LIKE ?
            ORDER BY name
        """, (f"%{keyword}%", f"%{keyword}%")).fetchall()


# ATTENDANCE FUNCTIONS

def mark_attendance(student_id, date, status):
    with connect() as con:
        con.execute("""
            INSERT INTO attendance (student_id, date, status)
            VALUES (?, ?, ?)
        """, (student_id, date, status))


def update_attendance(record_id, status):
    with connect() as con:
        con.execute("""
            UPDATE attendance
            SET status=?
            WHERE id=?
        """, (status, record_id))


def delete_attendance(record_id):
    with connect() as con:
        con.execute(
            "DELETE FROM attendance WHERE id=?",
            (record_id,)
        )


def get_attendance():
    with connect() as con:
        return con.execute("""
            SELECT attendance.id,
                   students.student_id,
                   students.name,
                   students.academic_year,
                   attendance.date,
                   attendance.status
            FROM attendance
            JOIN students
            ON attendance.student_id = students.student_id
            ORDER BY attendance.date DESC, students.name
        """).fetchall()


def search_attendance(keyword, date, status):
    query = """
        SELECT attendance.id,
               students.student_id,
               students.name,
               students.academic_year,
               attendance.date,
               attendance.status
        FROM attendance
        JOIN students
        ON attendance.student_id = students.student_id
        WHERE (students.student_id LIKE ?
               OR students.name LIKE ?)
    """
    values = [f"%{keyword}%", f"%{keyword}%"]

    if date:
        query += " AND attendance.date=?"
        values.append(date)

    if status != "All":
        query += " AND attendance.status=?"
        values.append(status)

    query += " ORDER BY attendance.date DESC, students.name"

    with connect() as con:
        return con.execute(query, values).fetchall()


def get_dashboard_counts(date):
    with connect() as con:
        total = con.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        present = con.execute("""
            SELECT COUNT(*) FROM attendance
            WHERE date=? AND status='Present'
        """, (date,)).fetchone()[0]

        absent = con.execute("""
            SELECT COUNT(*) FROM attendance
            WHERE date=? AND status='Absent'
        """, (date,)).fetchone()[0]

        late = con.execute("""
            SELECT COUNT(*) FROM attendance
            WHERE date=? AND status='Late'
        """, (date,)).fetchone()[0]

    return total, present, absent, late