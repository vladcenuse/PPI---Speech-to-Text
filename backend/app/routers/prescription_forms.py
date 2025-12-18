"""Prescription Forms endpoints (multiple per patient)"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_firestore_db
from app.firestore_helpers import get_next_id, doc_to_dict
from firebase_admin import firestore

router = APIRouter()


class PrescriptionFormBase(BaseModel):
    patient_id: int
    custom_name: Optional[str] = None
    date: str
    medications: Optional[str] = None
    dosage: Optional[str] = None
    instructions: Optional[str] = None
    follow_up: Optional[str] = None


class PrescriptionFormResponse(PrescriptionFormBase):
    id: int
    created_at: str
    updated_at: str


@router.get("/patient/{patient_id}", response_model=List[PrescriptionFormResponse])
async def get_prescription_forms(patient_id: int):
    """Get all prescription forms for a specific patient"""
    db = get_firestore_db()
    forms_ref = db.collection('prescription_forms')
    
    docs = forms_ref.where('patient_id', '==', patient_id).stream()
    
    forms = []
    for doc in docs:
        form_data = doc_to_dict(doc)
        if form_data:
            forms.append(form_data)
    
    # Sort by created_at descending in memory
    forms.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return forms


@router.get("/{form_id}", response_model=PrescriptionFormResponse)
async def get_prescription_form(form_id: int):
    """Get a single prescription form by ID"""
    db = get_firestore_db()
    forms_ref = db.collection('prescription_forms')
    
    doc_ref = forms_ref.document(str(form_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Form not found")
    
    return doc_to_dict(doc)


@router.post("/", response_model=PrescriptionFormResponse)
async def create_prescription_form(form_data: PrescriptionFormBase):
    """Create a new prescription form"""
    db = get_firestore_db()
    forms_ref = db.collection('prescription_forms')
    patients_ref = db.collection('patients')
    
    # Verify patient exists
    patient_doc = patients_ref.document(str(form_data.patient_id)).get()
    if not patient_doc.exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    current_time = datetime.now().isoformat()
    form_id = get_next_id('prescription_forms')
    
    form_dict = form_data.model_dump()
    form_dict['id'] = form_id
    form_dict['created_at'] = current_time
    form_dict['updated_at'] = current_time
    
    doc_ref = forms_ref.document(str(form_id))
    doc_ref.set(form_dict)
    
    return form_dict


@router.put("/{form_id}", response_model=PrescriptionFormResponse)
async def update_prescription_form(form_id: int, form_data: PrescriptionFormBase):
    """Update an existing prescription form"""
    db = get_firestore_db()
    forms_ref = db.collection('prescription_forms')
    
    # Fetch existing record to get created_at
    doc_ref = forms_ref.document(str(form_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Form not found")
    
    current_time = datetime.now().isoformat()
    created_at = doc.to_dict().get('created_at', current_time)
    
    update_data = form_data.model_dump()
    update_data['updated_at'] = current_time
    doc_ref.update(update_data)
    
    result = doc_ref.get().to_dict()
    result['id'] = form_id
    result['created_at'] = created_at
    
    return result


@router.delete("/{form_id}")
async def delete_prescription_form(form_id: int):
    """Delete a prescription form"""
    db = get_firestore_db()
    forms_ref = db.collection('prescription_forms')
    
    doc_ref = forms_ref.document(str(form_id))
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Form not found")
    
    doc_ref.delete()
    return {"message": "Form deleted successfully"}
