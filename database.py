import sqlite3
import bcrypt
import os
import pandas as pd

DATABASE = 'anemia_hospital.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # Create patient records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            patient_id TEXT,
            age INTEGER,
            gender TEXT,
            mode TEXT,
            prediction TEXT,
            confidence TEXT,
            doctor_username TEXT,
            timestamp TEXT
        )
    ''')

    # Create default admin account if none exists
    cursor.execute('SELECT * FROM users WHERE role = "admin"')
    if not cursor.fetchone():
        hashed = bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt())
        cursor.execute('''
            INSERT INTO users (full_name, username, password, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Administrator', 'admin', hashed.decode(), 'admin', '2024-01-01 00:00:00'))

    conn.commit()
    conn.close()

def verify_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
        return dict(user)
    return None

def register_doctor(full_name, username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute('''
            INSERT INTO users (full_name, username, password, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (full_name, username, hashed.decode(), 'doctor', 
              __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_doctors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, full_name, username, role, created_at FROM users WHERE role = "doctor"')
    doctors = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return doctors

def delete_doctor(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE username = ? AND role = "doctor"', (username,))
    conn.commit()
    conn.close()

def save_patient_record(record):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patient_records 
        (patient_name, patient_id, age, gender, mode, prediction, confidence, doctor_username, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        record['Patient Name'], record['Patient ID'], record['Age (months)'],
        record['Gender'], record['Mode'], record['Prediction'],
        record['Confidence'], record['Doctor'], record['Timestamp']
    ))
    conn.commit()
    conn.close()

def get_all_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patient_records ORDER BY timestamp DESC')
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return pd.DataFrame(records) if records else pd.DataFrame()

def get_doctor_records(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patient_records WHERE doctor_username = ? ORDER BY timestamp DESC', (username,))
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    import pandas as pd
    return pd.DataFrame(records) if records else pd.DataFrame()

def delete_record(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM patient_records WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

def delete_all_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM patient_records')
    conn.commit()
    conn.close()
