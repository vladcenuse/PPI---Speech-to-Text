from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class PatientBase(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    current_medications: Optional[str] = None
    blood_type: Optional[str] = None
    insurance_number: Optional[str] = None
    emergency_contact: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class MedicalDocumentBase(BaseModel):
    patient_id: int
    patient_name: str
    document_type: str
    document_id: str
    custom_name: Optional[str] = None
    date: str
    data: Dict[str, Any]


class MedicalDocumentCreate(MedicalDocumentBase):
    pass


class MedicalDocumentUpdate(MedicalDocumentBase):
    pass


class MedicalDocumentResponse(MedicalDocumentBase):
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class TranscriptionRequest(BaseModel):
    audio_file: bytes


class TranscriptionResponse(BaseModel):
    text: str


class ProcessRecordingRequest(BaseModel):
    fields: list[str]


class ProcessRecordingResponse(BaseModel):
    raw_transcript: str
    parsed_json: Dict[str, Any]


class DoctorBase(BaseModel):
    username: str


class DoctorCreate(DoctorBase):
    password: str
    confirm_password: str


class DoctorLogin(BaseModel):
    username: str
    password: str


class DoctorResponse(DoctorBase):
    id: int
    created_at: str
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    success: bool
    doctor_id: int
    username: str
    message: str
    token: str | None = None