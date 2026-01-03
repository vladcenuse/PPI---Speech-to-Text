from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.database import get_firestore_db
from app.firestore_helpers import get_next_id, doc_to_dict
from firebase_admin import firestore

router = APIRouter()


class NewPatientFormBase(BaseModel):
    patient_id: int
    custom_name: str = None
    date: str
    patient_name: str = None
    date_of_birth: str = None
    gender: str = None
    contact_info: str = None
    chief_complaint: str = None
    present_illness: str = None
    past_medical_history: str = None
    medications: str = None
    allergies: str = None
    family_history: str = None
    social_history: str = None
    vital_signs: str = None
    physical_exam: str = None
    assessment: str = None
    plan: str = None
    follow_up: str = None


class NewPatientFormResponse(NewPatientFormBase):
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


@router.get("/patient/{patient_id}", response_model=List[NewPatientFormResponse])
async def get_new_patient_form(patient_id: int):
    db = get_firestore_db()
    forms_ref = db.collection('new_patient_forms')
    
    docs = forms_ref.where('patient_id', '==', patient_id).stream()
    forms = []
    for doc in docs:
        form_data = doc_to_dict(doc)
        if form_data:
            forms.append(form_data)
    
    return forms


@router.get("/{form_id}", response_model=NewPatientFormResponse)
async def get_new_patient_form_by_id(form_id: int):
    db = get_firestore_db()
    forms_ref = db.collection('new_patient_forms')
    
    doc_ref = forms_ref.document(str(form_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Form not found")
    
    return doc_to_dict(doc)


@router.post("/", response_model=NewPatientFormResponse)
async def create_new_patient_form(form_data: NewPatientFormBase):
    db = get_firestore_db()
    forms_ref = db.collection('new_patient_forms')
    patients_ref = db.collection('patients')
    
    patient_doc = patients_ref.document(str(form_data.patient_id)).get()
    if not patient_doc.exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_docs = forms_ref.where('patient_id', '==', form_data.patient_id).limit(1).stream()
    existing_list = list(existing_docs)
    
    current_time = datetime.now().isoformat()
    
    if existing_list:
        existing_doc = existing_list[0]
        form_id = existing_doc.to_dict().get('id', int(existing_doc.id) if existing_doc.id.isdigit() else None)
        
        update_data = form_data.model_dump()
        update_data['patient_id'] = int(update_data['patient_id'])
        update_data['updated_at'] = current_time
        existing_doc.reference.update(update_data)
        
        result = existing_doc.reference.get().to_dict()
        result['id'] = form_id
        result['created_at'] = existing_doc.to_dict().get('created_at', current_time)
        return result
    else:
        form_id = get_next_id('new_patient_forms')
        
        form_dict = form_data.model_dump()
        form_dict['patient_id'] = int(form_dict['patient_id'])
        form_dict['id'] = form_id
        form_dict['created_at'] = current_time
        form_dict['updated_at'] = current_time
        
        doc_ref = forms_ref.document(str(form_id))
        doc_ref.set(form_dict)
        
        return form_dict


@router.put("/{form_id}", response_model=NewPatientFormResponse)
async def update_new_patient_form(form_id: int, form_data: NewPatientFormBase):
    db = get_firestore_db()
    forms_ref = db.collection('new_patient_forms')
    patients_ref = db.collection('patients')
    
    doc_ref = forms_ref.document(str(form_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Form not found")
    
    patient_doc = patients_ref.document(str(form_data.patient_id)).get()
    if not patient_doc.exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    current_time = datetime.now().isoformat()
    
    update_data = form_data.model_dump()
    update_data['patient_id'] = int(update_data['patient_id'])
    update_data['updated_at'] = current_time
    doc_ref.update(update_data)
    
    updated_doc = doc_ref.get()
    result = updated_doc.to_dict()
    result['id'] = form_id
    result['created_at'] = doc.to_dict().get('created_at', current_time)
    
    return result


@router.delete("/{form_id}")
async def delete_new_patient_form_by_id(form_id: int):
    db = get_firestore_db()
    forms_ref = db.collection('new_patient_forms')
    
    doc_ref = forms_ref.document(str(form_id))
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Form not found")
    
    doc_ref.delete()
    return {"message": "Form deleted successfully"}


@router.delete("/patient/{patient_id}")
async def delete_new_patient_form(patient_id: int):
    db = get_firestore_db()
    forms_ref = db.collection('new_patient_forms')
    
    docs = forms_ref.where('patient_id', '==', patient_id).stream()
    deleted_count = 0
    for doc in docs:
        doc.reference.delete()
        deleted_count += 1
    
    return {"message": "Form deleted successfully", "deleted_count": deleted_count}
