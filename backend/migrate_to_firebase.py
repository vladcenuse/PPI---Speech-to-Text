"""
Migration script to transfer data from SQLite to Firebase Firestore
Run this script after setting up Firebase credentials
"""
import sqlite3
import os
import json
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app, get_app

# Path to your SQLite database
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), 'medical_records.db')

# Path to your Firebase service account key JSON file
# You'll download this from Firebase Console
FIREBASE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'firebase-credentials.json')


def get_sqlite_connection():
    """Get SQLite database connection"""
    if not os.path.exists(SQLITE_DB_PATH):
        raise FileNotFoundError(f"SQLite database not found at {SQLITE_DB_PATH}")
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    if not os.path.exists(FIREBASE_CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"Firebase credentials file not found at {FIREBASE_CREDENTIALS_PATH}\n"
            "Please download your service account key from Firebase Console and save it as 'firebase-credentials.json'"
        )
    
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    
    # Check if app is already initialized
    try:
        initialize_app(cred)
    except ValueError:
        # App already initialized, that's fine
        pass
    
    return firestore.client()


def migrate_table(db, firestore_db, table_name, collection_name=None):
    """Migrate a single table from SQLite to Firestore"""
    if collection_name is None:
        collection_name = table_name
    
    print(f"\nMigrating table '{table_name}' to Firestore collection '{collection_name}'...")
    
    cursor = db.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if not cursor.fetchone():
        print(f"  ⚠️  Table '{table_name}' does not exist in SQLite database")
        return 0
    
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    if not rows:
        print(f"  No data found in {table_name}")
        return 0
    
    collection_ref = firestore_db.collection(collection_name)
    migrated_count = 0
    
    for row in rows:
        try:
            # Convert Row object to dictionary
            doc_data = dict(row)
            
            # Convert integer IDs to strings for Firestore document IDs
            doc_id = str(doc_data.get('id', migrated_count))
            
            # Remove 'id' from data (we'll use it as document ID)
            if 'id' in doc_data:
                del doc_data['id']
            
            # Add migration metadata
            doc_data['_migrated_at'] = datetime.now().isoformat()
            doc_data['_original_id'] = doc_id
            
            # Write to Firestore
            collection_ref.document(doc_id).set(doc_data)
            migrated_count += 1
        except Exception as e:
            print(f"  ✗ Error migrating document {migrated_count + 1}: {str(e)}")
            continue
    
    print(f"  ✓ Migrated {migrated_count} documents to '{collection_name}'")
    return migrated_count


def migrate_all():
    """Migrate all tables from SQLite to Firestore"""
    print("=" * 60)
    print("SQLite to Firebase Firestore Migration")
    print("=" * 60)
    
    # Initialize connections
    print("\n1. Connecting to SQLite database...")
    sqlite_db = get_sqlite_connection()
    print("   ✓ SQLite connection established")
    
    print("\n2. Initializing Firebase...")
    firestore_db = initialize_firebase()
    print("   ✓ Firebase initialized")
    
    # Define tables to migrate
    tables = [
        ('doctors', 'doctors'),
        ('patients', 'patients'),
        ('new_patient_forms', 'new_patient_forms'),
        ('medical_reports', 'medical_reports'),
        ('consultation_forms', 'consultation_forms'),
        ('prescription_forms', 'prescription_forms'),
    ]
    
    print("\n3. Starting migration...")
    total_migrated = 0
    
    for table_name, collection_name in tables:
        try:
            count = migrate_table(sqlite_db, firestore_db, table_name, collection_name)
            total_migrated += count
        except Exception as e:
            print(f"  ✗ Error migrating {table_name}: {str(e)}")
    
    sqlite_db.close()
    
    print("\n" + "=" * 60)
    print(f"Migration completed! Total documents migrated: {total_migrated}")
    print("=" * 60)
    
    return total_migrated


if __name__ == '__main__':
    try:
        migrate_all()
    except Exception as e:
        print(f"\n✗ Migration failed: {str(e)}")
        print("\nPlease check:")
        print("1. Firebase credentials file exists and is valid")
        print("2. SQLite database exists and is accessible")
        print("3. You have proper Firebase permissions")
        exit(1)

