"""
Doctor authentication endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, Request, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Optional
import sqlite3
from passlib.context import CryptContext
from app.models import DoctorCreate, DoctorLogin, DoctorResponse, LoginResponse
from app.database import get_db_connection

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Session timeout: 24 hours (can be changed)
SESSION_TIMEOUT_HOURS = 24

# In-memory session store (in production, use Redis or database)
# Format: {token: {"doctor_id": int, "created_at": datetime}}
active_sessions = {}


def hash_password(password: str) -> str:
    """Hash a password using pbkdf2_sha256"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def cleanup_expired_sessions():
    """Remove expired sessions from active_sessions"""
    now = datetime.now()
    expired_tokens = []
    for token, session_data in active_sessions.items():
        if isinstance(session_data, dict):
            created_at = session_data.get("created_at")
            if created_at and (now - created_at) > timedelta(hours=SESSION_TIMEOUT_HOURS):
                expired_tokens.append(token)
        # Handle old format (just doctor_id) - migrate to new format
        elif isinstance(session_data, int):
            # Old format, remove it (will be recreated on next login)
            expired_tokens.append(token)
    
    for token in expired_tokens:
        del active_sessions[token]
    
    if expired_tokens:
        print(f"[AUTH] Cleaned up {len(expired_tokens)} expired session(s)")


def get_current_doctor_id(request: Request) -> int:
    """Get current doctor ID from session token"""
    # Clean up expired sessions first
    cleanup_expired_sessions()
    
    authorization = request.headers.get("Authorization") or request.headers.get("authorization")
    
    if not authorization:
        print(f"[AUTH] No authorization header provided")
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    print(f"[AUTH] Received authorization header: {authorization[:30]}...")
    
    # Extract token from "Bearer <token>" format
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
    
    # Handle both old format (int) and new format (dict)
    if isinstance(session_data, dict):
        created_at = session_data.get("created_at")
        if created_at and (datetime.now() - created_at) > timedelta(hours=SESSION_TIMEOUT_HOURS):
            del active_sessions[token]
            print(f"[AUTH] Session expired")
            raise HTTPException(status_code=401, detail="Session expired or invalid")
        doctor_id = session_data.get("doctor_id")
    else:
        # Old format - just doctor_id
        doctor_id = session_data
    
    print(f"[AUTH] Found doctor_id: {doctor_id}")
    return doctor_id


@router.post("/register", response_model=LoginResponse)
async def register_doctor(doctor: DoctorCreate):
    """Register a new doctor account"""
    # Validate passwords match
    if doctor.password != doctor.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if len(doctor.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if username already exists
    cursor.execute('SELECT id FROM doctors WHERE username = ?', (doctor.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash password and create doctor
    password_hash = hash_password(doctor.password)
    current_time = datetime.now().isoformat()
    
    cursor.execute('''
        INSERT INTO doctors (username, password_hash, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    ''', (doctor.username, password_hash, current_time, current_time))
    
    doctor_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return LoginResponse(
        success=True,
        doctor_id=doctor_id,
        username=doctor.username,
        message="Account created successfully"
    )


@router.post("/login", response_model=LoginResponse)
async def login_doctor(doctor: DoctorLogin):
    """Login doctor and create session"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Find doctor by username
    cursor.execute('SELECT id, username, password_hash FROM doctors WHERE username = ?', (doctor.username,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    doctor_id, username, password_hash = row['id'], row['username'], row['password_hash']
    
    # Verify password
    if not verify_password(doctor.password, password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create session token (simple UUID-like token)
    import uuid
    session_token = str(uuid.uuid4())
    # Store session with creation time for timeout checking
    active_sessions[session_token] = {
        "doctor_id": doctor_id,
        "created_at": datetime.now()
    }
    
    # Return token in response (client will use it in Authorization header)
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
    """Logout doctor and invalidate session"""
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
    """Get current logged-in doctor info"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, created_at FROM doctors WHERE id = ?', (doctor_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return DoctorResponse(
        id=row['id'],
        username=row['username'],
        created_at=row['created_at']
    )

