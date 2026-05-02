import sqlite3

# create database (file auto-created)
conn = sqlite3.connect("patients.db", check_same_thread=False)
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    blood_pressure TEXT,
    date TEXT
)
""")

# insert new record
def insert_patient(name, bp, date):
    cursor.execute(
        "INSERT INTO patients (name, blood_pressure, date) VALUES (?, ?, ?)",
        (name, bp, date)
    )
    conn.commit()

# get latest record of patient
def get_patient_history(name):
    cursor.execute(
        "SELECT name, blood_pressure, date FROM patients WHERE name=? ORDER BY id DESC LIMIT 3",
        (name,)
    )
    return cursor.fetchall()