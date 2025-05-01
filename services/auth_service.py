from repositories.auth_repository import AuthRepository
from models.requests.auth_requests import RegisterRequest, LoginRequest, ResetPasswordRequest, ResetPasswordTokenRequest
from models.responses.auth_responses import TokenResponse
from fastapi import HTTPException, status, BackgroundTasks
from databases.models import User
from utils import email_utils, hash_utils, jwt_utils
import re, uuid
from datetime import datetime, timedelta

MAX_FAILED_ATTEMPTS = 3
SESSION_TIMEOUT_MINUTES = 15

async def register_user(request: RegisterRequest, background_tasks: BackgroundTasks, db):
    repo = AuthRepository(db)
    if repo.get_user_by_email(request.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if not hash_utils.validate_password_policy(request.password):
        raise HTTPException(status_code=400, detail="Weak password")

    hashed_password = hash_utils.hash_password(request.password)
    verification_token = str(uuid.uuid4())

    user = User(email=request.email, password=hashed_password, is_verified=False, verification_token=verification_token)
    repo.create_user(user)

    background_tasks.add_task(email_utils.send_verification_email, request.email, verification_token)
    return {"message": "User registered, please verify your email"}

async def verify_email(token: str, db):
    repo = AuthRepository(db)
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    user.is_verified = True
    user.verification_token = None
    return repo.update_user(user)

async def login_user(request: LoginRequest, db):
    repo = AuthRepository(db)
    user = repo.get_user_by_email(request.email)
    if not user or not hash_utils.verify_password(request.password, user.password):
        if user:
            user.failed_attempts += 1
            if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
                user.locked = True
            repo.update_user(user)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.locked:
        raise HTTPException(status_code=403, detail="Account locked")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    user.failed_attempts = 0
    user.last_login = datetime.utcnow()
    repo.update_user(user)
    token = jwt_utils.create_access_token({"sub": user.email}, expires_delta=timedelta(minutes=SESSION_TIMEOUT_MINUTES))
    return TokenResponse(access_token=token)

async def logout_user(token: str):
    # If using blacklisting or revocation, implement it here
    return {"message": "Logged out"}

async def reset_password(request: ResetPasswordRequest, background_tasks: BackgroundTasks, db):
    repo = AuthRepository(db)
    user = repo.get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reset_token = str(uuid.uuid4())
    user.reset_token = reset_token
    repo.update_user(user)
    background_tasks.add_task(email_utils.send_reset_password_email, user.email, reset_token)
    return {"message": "Reset password email sent"}

async def reset_password_with_token(request: ResetPasswordTokenRequest, db):
    repo = AuthRepository(db)
    user = db.query(User).filter(User.reset_token == request.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    if not hash_utils.validate_password_policy(request.new_password):
        raise HTTPException(status_code=400, detail="Weak password")
    user.password = hash_utils.hash_password(request.new_password)
    user.reset_token = None
    return repo.update_user(user)