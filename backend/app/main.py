from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import patients, documents, transcription, new_patient_forms, medical_reports, consultation_forms, prescription_forms
from app.database import check_and_init_db

# Initialize database
check_and_init_db()

app = FastAPI(
    title="Speech-to-Text Medical System API",
    description="Backend API for managing patients and medical documents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(patients.router, prefix="/api/patients", tags=["patients"])
app.include_router(new_patient_forms.router, prefix="/api/new-patient-forms", tags=["new-patient-forms"])
app.include_router(medical_reports.router, prefix="/api/medical-reports", tags=["medical-reports"])
app.include_router(consultation_forms.router, prefix="/api/consultation-forms", tags=["consultation-forms"])
app.include_router(prescription_forms.router, prefix="/api/prescription-forms", tags=["prescription-forms"])
app.include_router(transcription.router, prefix="/api", tags=["transcription"])


@app.get("/")
def read_root():
    return {
        "message": "Speech-to-Text Medical System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
