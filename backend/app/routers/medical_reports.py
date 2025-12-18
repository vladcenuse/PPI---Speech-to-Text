"""Medical Reports endpoints (multiple per patient)"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_firestore_db
from app.firestore_helpers import get_next_id, doc_to_dict
from firebase_admin import firestore

router = APIRouter()


class MedicalReportBase(BaseModel):
    patient_id: int
    custom_name: Optional[str] = None
    date: str
    chief_complaint: Optional[str] = None
    history_of_present_illness: Optional[str] = None
    physical_examination: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    recommendations: Optional[str] = None


class MedicalReportResponse(MedicalReportBase):
    id: int
    created_at: str
    updated_at: str


@router.get("/patient/{patient_id}", response_model=List[MedicalReportResponse])
async def get_medical_reports(patient_id: int):
    """Get all medical reports for a specific patient"""
    db = get_firestore_db()
    reports_ref = db.collection('medical_reports')
    
    docs = reports_ref.where('patient_id', '==', patient_id).stream()
    
    reports = []
    for doc in docs:
        report_data = doc_to_dict(doc)
        if report_data:
            reports.append(report_data)
    
    # Sort by created_at descending in memory
    reports.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return reports


@router.get("/{form_id}", response_model=MedicalReportResponse)
async def get_medical_report(form_id: int):
    """Get a single medical report by ID"""
    db = get_firestore_db()
    reports_ref = db.collection('medical_reports')
    
    doc_ref = reports_ref.document(str(form_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return doc_to_dict(doc)


@router.post("/", response_model=MedicalReportResponse)
async def create_medical_report(form_data: MedicalReportBase):
    """Create a new medical report"""
    db = get_firestore_db()
    reports_ref = db.collection('medical_reports')
    patients_ref = db.collection('patients')
    
    # Verify patient exists
    patient_doc = patients_ref.document(str(form_data.patient_id)).get()
    if not patient_doc.exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    current_time = datetime.now().isoformat()
    form_id = get_next_id('medical_reports')
    
    report_dict = form_data.model_dump()
    # Ensure patient_id is an integer (Firestore queries are type-sensitive)
    report_dict['patient_id'] = int(report_dict['patient_id'])
    report_dict['id'] = form_id
    report_dict['created_at'] = current_time
    report_dict['updated_at'] = current_time
    
    doc_ref = reports_ref.document(str(form_id))
    doc_ref.set(report_dict)
    
    return report_dict


@router.put("/{form_id}", response_model=MedicalReportResponse)
async def update_medical_report(form_id: int, form_data: MedicalReportBase):
    """Update an existing medical report"""
    db = get_firestore_db()
    reports_ref = db.collection('medical_reports')
    
    # Fetch existing record to get created_at
    doc_ref = reports_ref.document(str(form_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Report not found")
    
    current_time = datetime.now().isoformat()
    created_at = doc.to_dict().get('created_at', current_time)
    
    update_data = form_data.model_dump()
    # Ensure patient_id is an integer (Firestore queries are type-sensitive)
    update_data['patient_id'] = int(update_data['patient_id'])
    update_data['updated_at'] = current_time
    doc_ref.update(update_data)
    
    result = doc_ref.get().to_dict()
    result['id'] = form_id
    result['created_at'] = created_at
    
    return result


@router.delete("/{form_id}")
async def delete_medical_report(form_id: int):
    """Delete a medical report"""
    db = get_firestore_db()
    reports_ref = db.collection('medical_reports')
    
    doc_ref = reports_ref.document(str(form_id))
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Report not found")
    
    doc_ref.delete()
    return {"message": "Report deleted successfully"}
