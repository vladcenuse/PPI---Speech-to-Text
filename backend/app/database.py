import os
import json
import base64
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
from typing import Optional

FIREBASE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', 'firebase-credentials.json')

_db = None

def get_db_connection():
    return get_firestore_db()

def get_firestore_db():
    global _db
    if _db is None:
        firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        
        if firebase_creds_json:
            try:
                if firebase_creds_json.startswith('{'):
                    cred_dict = json.loads(firebase_creds_json)
                else:
                    decoded = base64.b64decode(firebase_creds_json).decode('utf-8')
                    cred_dict = json.loads(decoded)
                cred = credentials.Certificate(cred_dict)
            except Exception as e:
                raise ValueError(f"Failed to parse Firebase credentials from environment variable: {str(e)}")
        elif os.path.exists(FIREBASE_CREDENTIALS_PATH):
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        else:
            raise FileNotFoundError(
                f"Firebase credentials not found. Either set FIREBASE_CREDENTIALS_JSON environment variable "
                f"or place credentials file at {FIREBASE_CREDENTIALS_PATH}"
            )
        
        try:
            initialize_app(cred)
        except ValueError:
            pass
        
        _db = firestore.client()
    
    return _db


def check_and_init_db():
    db = get_firestore_db()
    
    try:
        doctors_ref = db.collection('doctors')
        doctors_count = len(list(doctors_ref.limit(1).stream()))
        
        patients_ref = db.collection('patients')
        patients_count = len(list(patients_ref.limit(1).stream()))
        
        print(f"Firebase ready. Found {doctors_count} doctors and {patients_count} patients.")
    except Exception as e:
        print(f"Firebase initialized. Collections will be created on first write.")


if __name__ == '__main__':
    check_and_init_db()

