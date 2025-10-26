"""
OpenAI Speech-to-Text transcription endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from openai import OpenAI
import os
from dotenv import load_dotenv
from app.models import TranscriptionResponse

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

# Lazy initialization function for OpenAI client
def get_openai_client():
    """Get OpenAI client, initializing it only when needed"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """
    Transcribe audio file using OpenAI Whisper
    """
    openai_client = get_openai_client()
    if not openai_client:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    try:
        # Read audio file
        audio_content = await audio_file.read()
        
        # Save to temporary file
        temp_file = f"temp_{audio_file.filename}"
        with open(temp_file, "wb") as f:
            f.write(audio_content)
        
        # Transcribe using OpenAI
        with open(temp_file, "rb") as f:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        return TranscriptionResponse(text=transcript.text)
    
    except Exception as e:
        # Clean up temporary file on error
        temp_file = f"temp_{audio_file.filename}"
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )


@router.get("/health")
async def transcription_health():
    """Check if transcription service is available"""
    openai_client = get_openai_client()
    if not openai_client:
        return {
            "status": "unavailable",
            "message": "OpenAI API key not configured"
        }
    return {
        "status": "available",
        "message": "Transcription service is ready"
    }

