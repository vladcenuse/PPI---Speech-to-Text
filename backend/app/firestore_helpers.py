"""
Helper functions for Firestore operations
"""
from firebase_admin import firestore
from app.database import get_firestore_db


def get_next_id(collection_name: str) -> int:
    """Get next ID from counter collection"""
    db = get_firestore_db()
    counter_ref = db.collection('_counters').document(collection_name)
    counter_doc = counter_ref.get()
    if counter_doc.exists:
        next_id = counter_doc.to_dict().get('count', 0) + 1
    else:
        next_id = 1
    counter_ref.set({'count': next_id}, merge=True)
    return next_id


def doc_to_dict(doc, include_id=True):
    """Convert Firestore document to dictionary"""
    if not doc.exists:
        return None
    data = doc.to_dict()
    if include_id:
        data['id'] = data.get('id', int(doc.id) if doc.id.isdigit() else None)
    return data

