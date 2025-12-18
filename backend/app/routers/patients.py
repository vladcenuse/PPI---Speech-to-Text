"""
Patient management endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from datetime import datetime
from typing import List, Optional
from app.models import PatientCreate, PatientUpdate, PatientResponse
from app.database import get_firestore_db
from app.routers.auth import get_current_doctor_id
from app.firestore_helpers import get_next_id
from firebase_admin import firestore

router = APIRouter()


@router.get("/", response_model=List[PatientResponse])
async def get_patients(doctor_id: int = Depends(get_current_doctor_id)):
    """Get all patients for the current doctor"""
    db = get_firestore_db()
    patients_ref = db.collection('patients')
    
    # Query patients by doctor_id (sort in memory to avoid index requirement)
    docs = patients_ref.where('doctor_id', '==', doctor_id).stream()
    
    patients = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data['id'] = doc_data.get('id', int(doc.id) if doc.id.isdigit() else None)
        patients.append(doc_data)
    
    # Sort by created_at descending in memory
    patients.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: int, doctor_id: int = Depends(get_current_doctor_id)):
    """Get a single patient by ID (only if owned by current doctor)"""
    db = get_firestore_db()
    patients_ref = db.collection('patients')
    
    # Get patient by ID and verify doctor_id
    doc_ref = patients_ref.document(str(patient_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    doc_data = doc.to_dict()
    if doc_data.get('doctor_id') != doctor_id:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    doc_data['id'] = patient_id
    return doc_data


@router.post("/", response_model=PatientResponse)
async def create_patient(patient: PatientCreate, doctor_id: int = Depends(get_current_doctor_id)):
    """Create a new patient (associated with current doctor)"""
    db = get_firestore_db()
    patients_ref = db.collection('patients')
    
    current_time = datetime.now().isoformat()
    patient_id = get_next_id('patients')
    
    patient_data = {
        'id': patient_id,
        'doctor_id': doctor_id,
        'name': patient.name,
        'age': patient.age,
        'gender': patient.gender,
        'date_of_birth': patient.date_of_birth,
        'phone': patient.phone,
        'email': patient.email,
        'address': patient.address,
        'medical_history': patient.medical_history,
        'allergies': patient.allergies,
        'current_medications': patient.current_medications,
        'blood_type': patient.blood_type,
        'insurance_number': patient.insurance_number,
        'emergency_contact': patient.emergency_contact,
        'created_at': current_time,
        'updated_at': current_time
    }
    
    doc_ref = patients_ref.document(str(patient_id))
    doc_ref.set(patient_data)
    
    return patient_data


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(patient_id: int, patient: PatientUpdate, doctor_id: int = Depends(get_current_doctor_id)):
    """Update an existing patient (only if owned by current doctor)"""
    db = get_firestore_db()
    patients_ref = db.collection('patients')
    
    # Check if patient exists and belongs to current doctor
    doc_ref = patients_ref.document(str(patient_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    doc_data = doc.to_dict()
    if doc_data.get('doctor_id') != doctor_id:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    current_time = datetime.now().isoformat()
    
    update_data = {
        'name': patient.name,
        'age': patient.age,
        'gender': patient.gender,
        'date_of_birth': patient.date_of_birth,
        'phone': patient.phone,
        'email': patient.email,
        'address': patient.address,
        'medical_history': patient.medical_history,
        'allergies': patient.allergies,
        'current_medications': patient.current_medications,
        'blood_type': patient.blood_type,
        'insurance_number': patient.insurance_number,
        'emergency_contact': patient.emergency_contact,
        'updated_at': current_time
    }
    
    doc_ref.update(update_data)
    
    # Get updated data
    updated_doc = doc_ref.get()
    result = updated_doc.to_dict()
    result['id'] = patient_id
    result['created_at'] = doc_data.get('created_at', current_time)
    
    return result


@router.delete("/{patient_id}")
async def delete_patient(patient_id: int, doctor_id: int = Depends(get_current_doctor_id)):
    """Delete a patient and all associated documents (only if owned by current doctor)"""
    db = get_firestore_db()
    
    # Check if patient exists and belongs to current doctor
    patients_ref = db.collection('patients')
    doc_ref = patients_ref.document(str(patient_id))
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    doc_data = doc.to_dict()
    if doc_data.get('doctor_id') != doctor_id:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    print(f"Deleting patient with ID: {patient_id}")
    
    # Delete all documents associated with this patient
    deleted_counts = {
        'prescription_forms': 0,
        'consultation_forms': 0,
        'medical_reports': 0,
        'new_patient_forms': 0
    }
    
    # Delete prescription forms
    prescription_ref = db.collection('prescription_forms')
    prescriptions = prescription_ref.where('patient_id', '==', patient_id).stream()
    for presc in prescriptions:
        presc.reference.delete()
        deleted_counts['prescription_forms'] += 1
    
    # Delete consultation forms
    consultation_ref = db.collection('consultation_forms')
    consultations = consultation_ref.where('patient_id', '==', patient_id).stream()
    for consult in consultations:
        consult.reference.delete()
        deleted_counts['consultation_forms'] += 1
    
    # Delete medical reports
    reports_ref = db.collection('medical_reports')
    reports = reports_ref.where('patient_id', '==', patient_id).stream()
    for report in reports:
        report.reference.delete()
        deleted_counts['medical_reports'] += 1
    
    # Delete new patient forms
    new_patient_ref = db.collection('new_patient_forms')
    new_forms = new_patient_ref.where('patient_id', '==', patient_id).stream()
    for form in new_forms:
        form.reference.delete()
        deleted_counts['new_patient_forms'] += 1
    
    # Finally delete the patient
    doc_ref.delete()
    print(f"Deleted patient {patient_id}")
    
    return {
        "message": "Patient and all associated documents deleted successfully",
        "deleted_documents": deleted_counts
    }
