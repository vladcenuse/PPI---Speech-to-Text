from fastapi import APIRouter, HTTPException, Depends, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from app.models import DoctorCreate, DoctorLogin, DoctorResponse, LoginResponse
from app.database import get_firestore_db
from app.firestore_helpers import get_next_id

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SESSION_TIMEOUT_HOURS = 24

active_sessions = {}


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def cleanup_expired_sessions():
    now = datetime.now()
    expired_tokens = []
    for token, session_data in active_sessions.items():
        if isinstance(session_data, dict):
            created_at = session_data.get("created_at")
            if created_at and (now - created_at) > timedelta(hours=SESSION_TIMEOUT_HOURS):
                expired_tokens.append(token)
        elif isinstance(session_data, int):
            expired_tokens.append(token)
    
    for token in expired_tokens:
        del active_sessions[token]
    
    if expired_tokens:
        print(f"[AUTH] Cleaned up {len(expired_tokens)} expired session(s)")


def get_current_doctor_id(request: Request) -> int:
    cleanup_expired_sessions()
    
    authorization = request.headers.get("Authorization") or request.headers.get("authorization")
    
    if not authorization:
        print(f"[AUTH] No authorization header provided")
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    print(f"[AUTH] Received authorization header: {authorization[:30]}...")
    
    try:
        if authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "").strip()
        else:
            token = authorization.strip()
        print(f"[AUTH] Extracted token: {token[:20]}...")
    except Exception as e:
        print(f"[AUTH] Error extracting token: {e}")
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    print(f"[AUTH] Active sessions count: {len(active_sessions)}")
    
    if token not in active_sessions:
        print(f"[AUTH] Token not found in active sessions")
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    session_data = active_sessions[token]
    
    if isinstance(session_data, dict):
        created_at = session_data.get("created_at")
        if created_at and (datetime.now() - created_at) > timedelta(hours=SESSION_TIMEOUT_HOURS):
            del active_sessions[token]
            print(f"[AUTH] Session expired")
            raise HTTPException(status_code=401, detail="Session expired or invalid")
        doctor_id = session_data.get("doctor_id")
    else:
        doctor_id = session_data
    
    print(f"[AUTH] Found doctor_id: {doctor_id}")
    return doctor_id


@router.post("/register", response_model=LoginResponse)
async def register_doctor(doctor: DoctorCreate):
    if doctor.password != doctor.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if len(doctor.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    db = get_firestore_db()
    doctors_ref = db.collection('doctors')
    
    existing = doctors_ref.where('username', '==', doctor.username).limit(1).stream()
    if list(existing):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    password_hash = hash_password(doctor.password)
    current_time = datetime.now().isoformat()
    
    doctor_id = get_next_id('doctors')
    
    doc_ref = doctors_ref.document(str(doctor_id))
    doc_ref.set({
        'id': doctor_id,
        'username': doctor.username,
        'password_hash': password_hash,
        'created_at': current_time,
        'updated_at': current_time
    })
    
    return LoginResponse(
        success=True,
        doctor_id=doctor_id,
        username=doctor.username,
        message="Account created successfully"
    )


@router.post("/login", response_model=LoginResponse)
async def login_doctor(doctor: DoctorLogin):
    db = get_firestore_db()
    doctors_ref = db.collection('doctors')
    
    docs = doctors_ref.where('username', '==', doctor.username).limit(1).stream()
    doc_list = list(docs)
    
    if not doc_list:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    doc = doc_list[0]
    doc_data = doc.to_dict()
    doctor_id = doc_data.get('id')
    if doctor_id is None:
        doctor_id = int(doc.id) if doc.id.isdigit() else None
    if doctor_id is None:
        raise HTTPException(status_code=500, detail="Invalid doctor record")
    username = doc_data.get('username', '')
    password_hash = doc_data.get('password_hash', '')
    
    if not verify_password(doctor.password, password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    import uuid
    session_token = str(uuid.uuid4())
    active_sessions[session_token] = {
        "doctor_id": doctor_id,
        "created_at": datetime.now()
    }
    
    bearer_token = f"Bearer {session_token}"
    response_data = LoginResponse(
        success=True,
        doctor_id=doctor_id,
        username=username,
        message="Login successful",
        token=bearer_token,
    )
    return response_data


@router.post("/logout")
async def logout_doctor(request: Request):
    authorization = request.headers.get("Authorization") or request.headers.get("authorization")
    
    if not authorization:
        return {"success": True, "message": "Already logged out"}
    
    try:
        if authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "").strip()
        else:
            token = authorization.strip()
        if token in active_sessions:
            del active_sessions[token]
    except:
        pass
    
    return {"success": True, "message": "Logged out successfully"}


@router.get("/me", response_model=DoctorResponse)
async def get_current_doctor(doctor_id: int = Depends(get_current_doctor_id)):
    db = get_firestore_db()
    doctors_ref = db.collection('doctors')
    
    docs = doctors_ref.where('id', '==', doctor_id).limit(1).stream()
    doc_list = list(docs)
    
    if not doc_list:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    doc = doc_list[0]
    doc_data = doc.to_dict()
    
    found_id = doc_data.get('id', doctor_id)
    
    return DoctorResponse(
        id=found_id,
        username=doc_data.get('username', ''),
        created_at=doc_data.get('created_at', '')
    )
