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
    
    import tempfile
    temp_file_path = None
    
    try:
        # Read audio file
        audio_content = await audio_file.read()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_file_obj:
            temp_file_obj.write(audio_content)
            temp_file_path = temp_file_obj.name
        
        # Get the filename
        filename = audio_file.filename or "recording.webm"
        
        # Transcribe using OpenAI - pass the file directly
        with open(temp_file_path, "rb") as audio_f:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_f,
                response_format="json"
            )
        
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        return TranscriptionResponse(text=transcript.text)
    
    except Exception as e:
        # Clean up temporary file on error
        import traceback
        error_trace = traceback.format_exc()
        print(f"Transcription error: {str(e)}")
        print(f"Traceback: {error_trace}")
        
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
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

