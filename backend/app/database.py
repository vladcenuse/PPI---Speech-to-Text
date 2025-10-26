"""
Database setup and configuration
"""
import sqlite3
import os
from datetime import datetime
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'medical_records.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def init_db():
    """Initialize database with tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            date_of_birth TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            medical_history TEXT,
            allergies TEXT,
            current_medications TEXT,
            blood_type TEXT,
            insurance_number TEXT,
            emergency_contact TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    # Create new_patient_forms table (unique per patient)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS new_patient_forms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL UNIQUE,
            custom_name TEXT,
            date TEXT NOT NULL,
            patient_name TEXT,
            date_of_birth TEXT,
            gender TEXT,
            contact_info TEXT,
            chief_complaint TEXT,
            present_illness TEXT,
            past_medical_history TEXT,
            medications TEXT,
            allergies TEXT,
            family_history TEXT,
            social_history TEXT,
            vital_signs TEXT,
            physical_exam TEXT,
            assessment TEXT,
            plan TEXT,
            follow_up TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
        )
    ''')
    
    # Create medical_reports table (multiple per patient)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            custom_name TEXT,
            date TEXT NOT NULL,
            chief_complaint TEXT,
            history_of_present_illness TEXT,
            physical_examination TEXT,
            diagnosis TEXT,
            treatment TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
        )
    ''')
    
    # Create consultation_forms table (multiple per patient)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultation_forms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            custom_name TEXT,
            date TEXT NOT NULL,
            symptoms TEXT,
            vital_signs TEXT,
            assessment TEXT,
            plan TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
        )
    ''')
    
    # Create prescription_forms table (multiple per patient)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescription_forms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            custom_name TEXT,
            date TEXT NOT NULL,
            medications TEXT,
            dosage TEXT,
            instructions TEXT,
            follow_up TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")


def check_and_init_db():
    """Check if database exists, if not create and populate with mock data"""
    if not os.path.exists(DB_PATH):
        print("Database not found. Creating new database...")
        init_db()
        populate_mock_data()
    else:
        print("Database exists. Checking tables...")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patients'")
        if not cursor.fetchone():
            print("Tables not found. Initializing database...")
            init_db()
            populate_mock_data()
        else:
            print("Database and tables exist.")
        
        conn.close()


def populate_mock_data():
    """Populate database with mock data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    current_time = datetime.now().isoformat()
    
    # Insert mock patients
    mock_patients = [
        {
            'name': 'Ion Popescu',
            'age': 45,
            'gender': 'Male',
            'phone': '0712345678',
            'email': 'ion.popescu@email.com',
            'medical_history': 'Arterial hypertension, type 2 diabetes',
            'allergies': 'Penicillin',
            'current_medications': 'Metformin 500mg, Lisinopril 10mg',
            'blood_type': 'A+',
            'address': 'Bucharest, Romania'
        },
        {
            'name': 'Maria Ionescu',
            'age': 32,
            'gender': 'Female',
            'phone': '0798765432',
            'email': 'maria.ionescu@email.com',
            'medical_history': 'Iron deficiency anemia',
            'allergies': 'No known allergies',
            'current_medications': 'Iron supplements',
            'blood_type': 'O+',
            'address': 'Cluj-Napoca, Romania'
        },
        {
            'name': 'Gheorghe Dumitrescu',
            'age': 67,
            'gender': 'Male',
            'phone': '0711111111',
            'medical_history': 'Ischemic heart disease, arthritis',
            'allergies': 'Aspirin',
            'current_medications': 'Aspirin 100mg, Atorvastatin 20mg',
            'blood_type': 'B+',
            'address': 'Timisoara, Romania'
        }
    ]
    
    for patient in mock_patients:
        cursor.execute('''
            INSERT INTO patients (
                name, age, gender, phone, email, address, 
                medical_history, allergies, current_medications, blood_type,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patient['name'], patient['age'], patient['gender'],
            patient['phone'], patient.get('email', ''), patient.get('address', ''),
            patient['medical_history'], patient['allergies'], patient['current_medications'],
            patient['blood_type'], current_time, current_time
        ))
    
    conn.commit()
    conn.close()
    print("Mock data populated successfully")


if __name__ == '__main__':
    check_and_init_db()

