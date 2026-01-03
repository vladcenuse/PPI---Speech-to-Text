from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
import json
from app.models import MedicalDocumentCreate, MedicalDocumentUpdate, MedicalDocumentResponse
from app.database import get_firestore_db
from app.firestore_helpers import get_next_id, doc_to_dict
from firebase_admin import firestore

router = APIRouter()


@router.get("/", response_model=List[MedicalDocumentResponse])
async def get_documents():
    db = get_firestore_db()
    docs_ref = db.collection('medical_documents')
    
    docs = docs_ref.order_by('created_at', direction=firestore.Query.DESCENDING).stream()
    
    documents = []
    for doc in docs:
        doc_data = doc_to_dict(doc)
        if doc_data:
            if isinstance(doc_data.get('data'), str):
                try:
                    doc_data['data'] = json.loads(doc_data['data'])
                except:
                    doc_data['data'] = {}
            documents.append(doc_data)
    
    return documents


@router.get("/patient/{patient_id}", response_model=List[MedicalDocumentResponse])
async def get_documents_by_patient(patient_id: int):
    db = get_firestore_db()
    docs_ref = db.collection('medical_documents')
    
    docs = docs_ref.where('patient_id', '==', patient_id).stream()
    
    documents = []
    for doc in docs:
        doc_data = doc_to_dict(doc)
        if doc_data:
            if isinstance(doc_data.get('data'), str):
                try:
                    doc_data['data'] = json.loads(doc_data['data'])
                except:
                    doc_data['data'] = {}
            documents.append(doc_data)
    
    documents.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return documents


@router.get("/{document_id}", response_model=MedicalDocumentResponse)
async def get_document(document_id: int):
    db = get_firestore_db()
    docs_ref = db.collection('medical_documents')
    
    doc_ref = docs_ref.document(str(document_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc_data = doc_to_dict(doc)
    if isinstance(doc_data.get('data'), str):
        try:
            doc_data['data'] = json.loads(doc_data['data'])
        except:
            doc_data['data'] = {}
    
    return doc_data


@router.post("/", response_model=MedicalDocumentResponse)
async def create_document(document: MedicalDocumentCreate):
    db = get_firestore_db()
    docs_ref = db.collection('medical_documents')
    patients_ref = db.collection('patients')
    
    patient_doc = patients_ref.document(str(document.patient_id)).get()
    if not patient_doc.exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    current_time = datetime.now().isoformat()
    document_id = get_next_id('medical_documents')
    
    doc_dict = document.model_dump()
    doc_dict['id'] = document_id
    doc_dict['data'] = json.dumps(doc_dict['data']) if isinstance(doc_dict['data'], dict) else doc_dict['data']
    doc_dict['created_at'] = current_time
    doc_dict['updated_at'] = current_time
    
    doc_ref = docs_ref.document(str(document_id))
    doc_ref.set(doc_dict)
    
    result = doc_dict.copy()
    result['data'] = json.loads(result['data']) if isinstance(result['data'], str) else result['data']
    return result


@router.put("/{document_id}", response_model=MedicalDocumentResponse)
async def update_document(document_id: int, document: MedicalDocumentUpdate):
    db = get_firestore_db()
    docs_ref = db.collection('medical_documents')
    
    doc_ref = docs_ref.document(str(document_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Document not found")
    
    current_time = datetime.now().isoformat()
    created_at = doc.to_dict().get('created_at', current_time)
    
    update_data = document.model_dump()
    update_data['data'] = json.dumps(update_data['data']) if isinstance(update_data['data'], dict) else update_data['data']
    update_data['updated_at'] = current_time
    
    doc_ref.update(update_data)
    
    result = doc_ref.get().to_dict()
    result['id'] = document_id
    result['created_at'] = created_at
    result['data'] = json.loads(result['data']) if isinstance(result.get('data'), str) else result.get('data', {})
    
    return result


@router.delete("/{document_id}")
async def delete_document(document_id: int):
    db = get_firestore_db()
    docs_ref = db.collection('medical_documents')
    
    doc_ref = docs_ref.document(str(document_id))
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc_ref.delete()
    return {"message": "Document deleted successfully"}
