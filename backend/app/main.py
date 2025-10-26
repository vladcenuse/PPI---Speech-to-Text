from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import patients, documents, transcription
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
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(patients.router, prefix="/api/patients", tags=["patients"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
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
