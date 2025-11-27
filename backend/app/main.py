import os
import json
import re
from rapidfuzz import fuzz
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, APIRouter
from pydantic import BaseModel
from deepgram import DeepgramClient
from fastapi.middleware.cors import CORSMiddleware

def check_and_init_db():
    print("Database initialization mocked.")
    pass

class MockRouter:
    def __init__(self, name):
        self.router = APIRouter()
        print(f"Mocking router: {name}")

patients = MockRouter("patients")
documents = MockRouter("documents")
new_patient_forms = MockRouter("new_patient_forms")
medical_reports = MockRouter("medical_reports")
consultation_forms = MockRouter("consultation_forms")
prescription_forms = MockRouter("prescription_forms")

class TranscriptionResponse(BaseModel):
    text: str

class ParsedRecordingResponse(BaseModel):
    raw_transcript: str
    parsed_json: dict

def safe_encode_str(s):
    """Safely encode a string to ASCII, replacing problematic characters"""
    try:
        if isinstance(s, bytes):
            s = s.decode('utf-8', errors='replace')
        return str(s).encode('ascii', 'replace').decode('ascii')
    except:
        return repr(s)

def safe_print(msg):
    """Safely print a message, handling Unicode encoding"""
    try:
        safe_msg = safe_encode_str(msg)
        print(safe_msg)
    except:
        print(repr(msg))

# Helper to safely extract exception info without calling str() or repr() on exception object
def extract_exception_info(exc):
    """Extract exception information without calling str() or repr() on exception to avoid encoding issues"""
    exc_type = type(exc).__name__
    exc_args = []
    
    try:
        # Try to get args safely - NEVER call str() or repr() on the exception object itself
        if hasattr(exc, 'args') and exc.args:
            for arg in exc.args:
                try:
                    # Try to encode each arg
                    if isinstance(arg, str):
                        exc_args.append(safe_encode_str(arg))
                    elif isinstance(arg, bytes):
                        exc_args.append(safe_encode_str(arg.decode('utf-8', errors='replace')))
                    else:
                        # For non-string args, try to convert safely
                        # But wrap in try-except to catch encoding errors
                        try:
                            # Try str() but catch encoding errors
                            arg_str = str(arg)
                            exc_args.append(safe_encode_str(arg_str))
                        except UnicodeEncodeError:
                            # If str() fails due to encoding, try repr() on the arg (not the exception)
                            try:
                                arg_repr = repr(arg)
                                exc_args.append(safe_encode_str(arg_repr))
                            except:
                                exc_args.append("(unable to encode arg)")
                        except Exception:
                            # Any other error converting arg
                            exc_args.append("(unable to convert arg)")
                except Exception:
                    # If anything fails, just skip this arg
                    exc_args.append("(error encoding arg)")
    except Exception:
        # If we can't even access args, that's okay
        pass
    
    # Build message from parts - NEVER use repr(exc) as it might call str(exc) internally
    if exc_args:
        msg = ' '.join(exc_args)
    else:
        msg = exc_type
    
    return exc_type, msg

def transcribe_audio_bytes_ro(
    audio_content: bytes, 
    content_type: str
) -> TranscriptionResponse:
    
    DEEPGRAM_API_KEY = "4700b39b6fffa69b829bc2510b31859a60081fe3"
    
    # Initialize DeepgramClient
    safe_print(f"Initializing DeepgramClient with API key (length: {len(DEEPGRAM_API_KEY)})")
    safe_print(f"API key starts with: {DEEPGRAM_API_KEY[:10]}...")
    
    deepgram_client = None
    try:
        # Initialize with explicit keyword argument
        deepgram_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
        safe_print("[SUCCESS] DeepgramClient initialized successfully")
    except Exception as init_error:
        error_type, error_msg = extract_exception_info(init_error)
        safe_print(f"[ERROR] Failed to initialize DeepgramClient: {error_type}")
        raise RuntimeError(f"Failed to initialize Deepgram client: {error_msg}")

    # Call Deepgram API
    try:
        safe_print("Calling Deepgram API...")
        response = deepgram_client.listen.v1.media.transcribe_file(
            request=audio_content,
            smart_format=True,
            model="whisper",
            language="ro"
        )
        
        safe_print("Deepgram API call successful, extracting transcript...")
        
        # Safely extract transcript, handling potential None values
        try:
            transcript_text = response.results.channels[0].alternatives[0].transcript
        except (AttributeError, IndexError, KeyError) as e:
            safe_print("Warning: Could not extract transcript from Deepgram response")
            raise RuntimeError("Nu s-a putut extrage transcrierea din răspunsul API. Vă rugăm să încercați din nou.")
        
        # Handle None or missing transcript
        if transcript_text is None:
            safe_print("Warning: None transcript received from Deepgram")
            raise RuntimeError("Nu s-a detectat niciun vorbire în înregistrare. Vă rugăm să înregistrați din nou.")
        
        # Validate transcript - check if it's empty or contains generic placeholder text
        transcript_text = str(transcript_text).strip()
        if not transcript_text:
            safe_print("Warning: Empty transcript received from Deepgram")
            raise RuntimeError("Nu s-a detectat niciun vorbire în înregistrare. Vă rugăm să înregistrați din nou.")
        
        # Check for common generic/placeholder phrases that indicate unclear or no speech
        transcript_lower = transcript_text.lower()
        generic_phrases = [
            "vă mulțumesc",
            "mulțumesc pentru",
            "thank you",
            "thanks for",
            "pentru vizionare",
            "for watching",
            "pentru atenție",
            "for your attention",
            "mulțumesc frumos"
        ]
        
        # If transcript only contains generic phrases and is short, it's likely invalid
        if any(phrase in transcript_lower for phrase in generic_phrases) and len(transcript_text) < 50:
            safe_print(f"Warning: Generic placeholder transcript detected: {transcript_text[:100]}")
            raise RuntimeError("Vorbirea nu a putut fi recunoscută clar sau înregistrarea conține doar zgomot. Vă rugăm să vorbiți clar despre măsurătorile ecocardiografice și să înregistrați din nou.")
        
        # Check if transcript is too short (likely noise or unclear)
        if len(transcript_text) < 10:
            safe_print(f"Warning: Very short transcript: {transcript_text}")
            raise RuntimeError("Înregistrarea este prea scurtă sau neclară. Vă rugăm să înregistrați din nou.")
        
        safe_print(f"Transcript validated successfully: {len(transcript_text)} characters")
        return TranscriptionResponse(text=transcript_text)
        
    except RuntimeError as e:
        # If it's already a RuntimeError (like our validation errors), preserve it with UTF-8
        # Only encode to ASCII for console printing
        if hasattr(e, 'args') and e.args and isinstance(e.args[0], str):
            error_msg_utf8 = e.args[0]
            error_msg_ascii = safe_encode_str(error_msg_utf8)
            safe_print(f"RuntimeError: {error_msg_ascii}")
            raise  # Re-raise the original RuntimeError with UTF-8 message
        else:
            # Fallback if structure is different
            error_type, error_msg = extract_exception_info(e)
            safe_print(f"RuntimeError: {error_msg}")
            raise RuntimeError(error_msg)
    except Exception as e:
        # Extract exception info safely without calling str()
        error_type, error_msg = extract_exception_info(e)
        
        safe_print(f"Deepgram API Error - Type: {error_type}")
        
        # Check if it's a Deepgram-related error
        if "deepgram" in error_msg.lower() or "api" in error_msg.lower() or "deepgram" in error_type.lower():
            raise RuntimeError(f"Deepgram API Error during transcription: {error_msg}")
        else:
            raise RuntimeError(f"An unexpected error occurred during transcription: {error_msg}")

def extract_value_after_field(transcript: str, field_end_pos: int, all_field_names: list) -> str:
    """
    Extract the value (number + unit) immediately after a field name.
    Stops when it finds another field name or extracts a complete value.
    """
    number_words = {
        'zero': '0', 'unu': '1', 'una': '1', 'doi': '2', 'două': '2',
        'trei': '3', 'patru': '4', 'cinci': '5', 'șase': '6', 'sase': '6',
        'șapte': '7', 'sapte': '7', 'opt': '8', 'nouă': '9', 'noua': '9',
        'zece': '10', 'unsprezece': '11', 'doisprezece': '12', 'treisprezece': '13',
        'paisprezece': '14', 'cincisprezece': '15', 'șaisprezece': '16',
        'șaptesprezece': '17', 'optsprezece': '18', 'nouăsprezece': '19', 'nouasprezece': '19',
        'douăzeci': '20', 'douazeci': '20'
    }
    
    units = ['milimetri', 'centimetri', 'metri', 'mm', 'cm', 'm']
    
    remaining_text = transcript[field_end_pos:].strip()
    remaining_lower = remaining_text.lower()
    
    next_field_pos = len(remaining_text)
    normalized_all_fields = [f.lower() for f in all_field_names]
    
    for field_name in normalized_all_fields:
        field_pos = remaining_lower.find(field_name)
        if field_pos != -1 and field_pos < next_field_pos:
            next_field_pos = field_pos
    
    search_text = remaining_text[:next_field_pos].strip()
    search_lower = search_text.lower()
    
    pattern1 = r'(\d+(?:[.,]\d+)?)\s*(milimetri|centimetri|metri|mm|cm|m)\b'
    match1 = re.search(pattern1, search_lower, re.IGNORECASE)
    if match1:
        original_match = re.search(pattern1, search_text, re.IGNORECASE)
        if original_match:
            value = original_match.group(0).strip()
            parts = value.split()
            if len(parts) >= 2:
                if parts[1].lower() in units or parts[1].lower().replace('mm', '').replace('cm', '').replace('m', '') == '':
                    return f"{parts[0]} {parts[1]}"
            return value
    
    for word, digit in number_words.items():
        pattern2 = rf'\b{re.escape(word)}\s+(milimetri|centimetri|metri|mm|cm|m)\b'
        match2 = re.search(pattern2, search_lower)
        if match2:
            original_match = re.search(pattern2, search_text, re.IGNORECASE)
            if original_match:
                value = original_match.group(0).strip()
                parts = value.split()
                if len(parts) >= 2 and parts[0].lower() in number_words:
                    return f"{number_words[parts[0].lower()]} {parts[1]}"
                return value
    
    pattern3 = r'\b(\d+(?:[.,]\d+)?)\b'
    match3 = re.search(pattern3, search_lower)
    if match3:
        original_match = re.search(pattern3, search_text, re.IGNORECASE)
        if original_match:
            num = original_match.group(1)
            num_start = original_match.start()
            
            after_num_text = search_text[original_match.end():original_match.end()+10].strip()
            unit_match = re.search(r'\b(milimetri|centimetri|metri|mm|cm|m)\b', after_num_text, re.IGNORECASE)
            
            if unit_match:
                return f"{num} {unit_match.group(0)}"
            else:
                if num_start < 30:
                    return num
    
    first_part = search_lower[:30] if len(search_lower) > 30 else search_lower
    for word, digit in number_words.items():
        pattern4 = rf'\b{re.escape(word)}\b'
        match4 = re.search(pattern4, first_part)
        if match4:
            word_end_in_full = match4.end()
            after_word = search_lower[word_end_in_full:word_end_in_full+15].strip()
            unit_match = re.search(r'\b(milimetri|centimetri|metri|mm|cm|m)\b', after_word)
            if unit_match:
                return f"{digit} {unit_match.group(0)}"
            else:
                return digit
    
    return ""

def fuzzy_transcription_to_json(transcription_string: str, field_list: list, threshold: int = 50) -> str:
    """
    Parse transcription to extract field values.
    For each field name found, extracts only the value (number + unit) immediately following it.
    """
    normalized_transcription = transcription_string.lower()
    
    matched_fields = {}
    
    for expected_field in field_list:
        normalized_expected_field = expected_field.lower()
        
        best_match_key = None
        best_score = -1
        best_start_pos = -1
        best_end_pos = -1
        
        len_expected = len(normalized_expected_field)
        min_len = max(1, int(len_expected * 0.5))
        max_len = int(len_expected * 2.5)

        for start in range(len(normalized_transcription)):
            end_limit = min(start + max_len, len(normalized_transcription)) + 1
            
            for end in range(start + min_len, end_limit):
                segment = normalized_transcription[start:end]
                
                score = fuzz.ratio(normalized_expected_field, segment)
                
                if score > best_score and score >= threshold:
                    best_score = score
                    if abs(len(segment) - len_expected) < len_expected * 0.6:
                        best_match_key = transcription_string[start:end].strip()
                        best_start_pos = start
                        best_end_pos = end
            
        if best_match_key:
            matched_fields[expected_field] = (best_match_key, best_start_pos, best_end_pos)
    
    result_dict = {}
    
    for expected_field, (matched_key, start_pos, end_pos) in matched_fields.items():
        value = extract_value_after_field(
            transcription_string,
            end_pos,
            field_list
        )
        result_dict[expected_field] = value
    
    for field in field_list:
        if field not in result_dict:
            result_dict[field] = ""
            
    return json.dumps(result_dict, indent=4, ensure_ascii=False)


check_and_init_db()

app = FastAPI(
    title="Speech-to-Text Medical System API",
    description="Backend API for managing patients and medical documents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "http://localhost:5174",
        "http://127.0.0.1:5173",  
        "http://127.0.0.1:5174"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router, prefix="/api/patients", tags=["patients"])
app.include_router(new_patient_forms.router, prefix="/api/new-patient-forms", tags=["new-patient-forms"])
app.include_router(medical_reports.router, prefix="/api/medical-reports", tags=["medical-reports"])
app.include_router(consultation_forms.router, prefix="/api/consultation-forms", tags=["consultation-forms"])
app.include_router(prescription_forms.router, prefix="/api/prescription-forms", tags=["prescription-forms"])

@app.post("/api/process-recording", response_model=ParsedRecordingResponse, tags=["transcription"])
async def process_recording_endpoint(
    audio_file: UploadFile = File(...),
    fields_json: str = Form(...) 
):
    
    try:
        fields_data = json.loads(fields_json)
        target_fields = fields_data.get("fields", [])
        
        if not target_fields or not isinstance(target_fields, list):
            raise HTTPException(
                status_code=400, 
                detail="Invalid 'fields' array provided in JSON string."
            )
            
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="The 'fields_json' parameter must be a valid JSON string."
        )

    try:
        audio_content = await audio_file.read()
        
        safe_print(f"Processing audio file: {audio_file.filename}, size: {len(audio_content)} bytes")
        safe_print(f"Content type: {audio_file.content_type}")
        
        transcript_response = transcribe_audio_bytes_ro(
            audio_content,
            audio_file.content_type
        )
        raw_transcript = transcript_response.text
        safe_print(f"Transcription successful, length: {len(raw_transcript)} chars")

        parsed_json_string = fuzzy_transcription_to_json(
            raw_transcript, 
            target_fields
        )
        parsed_json = json.loads(parsed_json_string)
        
        return ParsedRecordingResponse(
            raw_transcript=raw_transcript,
            parsed_json=parsed_json
        )
    
    except RuntimeError as e:
        # For RuntimeError, extract the message directly (it's already in Romanian and safe)
        # RuntimeError messages are user-facing, so preserve UTF-8 encoding for HTTP responses
        # Only encode to ASCII for console printing
        if hasattr(e, 'args') and e.args and isinstance(e.args[0], str):
            # Preserve original UTF-8 string for HTTP response
            error_msg_utf8 = e.args[0]
            # Use ASCII-encoded version only for console
            error_msg_ascii = safe_encode_str(error_msg_utf8)
            safe_print(f"Processing failed: {error_msg_ascii}")
            raise HTTPException(
                status_code=500,
                detail=error_msg_utf8  # Use UTF-8 version for HTTP response
            )
        else:
            # Fallback to extract_exception_info if structure is different
            error_type, error_msg = extract_exception_info(e)
            safe_print(f"Processing failed: {error_type}")
            raise HTTPException(
                status_code=500,
                detail=error_msg
            )
    except Exception as e:
        # Extract exception info safely without calling str()
        error_type, error_msg = extract_exception_info(e)
        safe_print(f"An unexpected error occurred: {error_type}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {error_msg}"  # Use message directly
        )


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