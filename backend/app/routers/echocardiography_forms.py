"""
Echocardiography form management endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.database import get_firestore_db
from app.firestore_helpers import get_next_id, doc_to_dict
from firebase_admin import firestore

router = APIRouter()


class EchocardiographyFormBase(BaseModel):
    patient_id: int
    custom_name: Optional[str] = None
    date: str
    aorta_la_inel: Optional[str] = None
    aorta_la_sinusur_levart_sagva: Optional[str] = None
    aorta_ascendenta: Optional[str] = None
    as_value: Optional[str] = Field(None, alias='as')
    ventricul_drept: Optional[str] = None
    atriu_stang: Optional[str] = None
    vd: Optional[str] = None
    
    class Config:
        populate_by_name = True


class EchocardiographyFormResponse(EchocardiographyFormBase):
    id: int
    created_at: str
    updated_at: str


@router.get("/patient/{patient_id}", response_model=List[EchocardiographyFormResponse])
async def get_echocardiography_forms(patient_id: int):
    """Get all echocardiography forms for a specific patient"""
    db = get_firestore_db()
    forms_ref = db.collection('echocardiography_forms')
    
    docs = forms_ref.where('patient_id', '==', patient_id).stream()
    
    forms = []
    for doc in docs:
        form_data = doc_to_dict(doc)
        if form_data:
            forms.append(form_data)
    
    # Sort by created_at descending in memory
    forms.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return forms


@router.get("/{form_id}", response_model=EchocardiographyFormResponse)
async def get_echocardiography_form(form_id: int):
    """Get a single echocardiography form by ID"""
    db = get_firestore_db()
    forms_ref = db.collection('echocardiography_forms')
    
    doc_ref = forms_ref.document(str(form_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Form not found")
    
    return doc_to_dict(doc)


@router.post("/", response_model=EchocardiographyFormResponse)
async def create_echocardiography_form(form_data: EchocardiographyFormBase):
    """Create a new echocardiography form"""
    db = get_firestore_db()
    forms_ref = db.collection('echocardiography_forms')
    patients_ref = db.collection('patients')
    
    # Verify patient exists
    patient_doc = patients_ref.document(str(form_data.patient_id)).get()
    if not patient_doc.exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    current_time = datetime.now().isoformat()
    form_id = get_next_id('echocardiography_forms')
    
    form_dict = form_data.model_dump(by_alias=True)
    # Ensure patient_id is an integer (Firestore queries are type-sensitive)
    form_dict['patient_id'] = int(form_dict['patient_id'])
    form_dict['id'] = form_id
    form_dict['created_at'] = current_time
    form_dict['updated_at'] = current_time
    
    doc_ref = forms_ref.document(str(form_id))
    doc_ref.set(form_dict)
    
    return form_dict


@router.put("/{form_id}", response_model=EchocardiographyFormResponse)
async def update_echocardiography_form(form_id: int, form_data: EchocardiographyFormBase):
    """Update an existing echocardiography form"""
    db = get_firestore_db()
    forms_ref = db.collection('echocardiography_forms')
    
    # Fetch existing record to get created_at
    doc_ref = forms_ref.document(str(form_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Form not found")
    
    current_time = datetime.now().isoformat()
    created_at = doc.to_dict().get('created_at', current_time)
    
    update_data = form_data.model_dump(by_alias=True)
    # Ensure patient_id is an integer (Firestore queries are type-sensitive)
    update_data['patient_id'] = int(update_data['patient_id'])
    update_data['updated_at'] = current_time
    doc_ref.update(update_data)
    
    result = doc_ref.get().to_dict()
    result['id'] = form_id
    result['created_at'] = created_at
    
    return result


@router.delete("/{form_id}")
async def delete_echocardiography_form(form_id: int):
    """Delete an echocardiography form"""
    db = get_firestore_db()
    forms_ref = db.collection('echocardiography_forms')
    
    doc_ref = forms_ref.document(str(form_id))
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Form not found")
    
    doc_ref.delete()
    return {"message": "Form deleted successfully"}

