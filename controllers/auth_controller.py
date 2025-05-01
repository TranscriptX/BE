from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from models.requests.auth_requests import RegisterRequest, LoginRequest, ResetPasswordRequest, ResetPasswordTokenRequest
from models.responses.auth_responses import TokenResponse
from services import auth_service
from sqlalchemy.orm import Session
from databases.dependencies import get_session

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=dict)
async def register(request: RegisterRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_session)):
    return await auth_service.register_user(request, background_tasks, db)

@router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_session)):
    return await auth_service.verify_email(token, db)

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_session)):
    return await auth_service.login_user(request, db)

@router.post("/logout", response_model=dict)
async def logout(token: str):
    return await auth_service.logout_user(token)

@router.post("/reset-password", response_model=dict)
async def reset_password(request: ResetPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_session)):
    return await auth_service.reset_password(request, background_tasks, db)

@router.post("/reset-password-token", response_model=dict)
async def reset_password_token(request: ResetPasswordTokenRequest, db: Session = Depends(get_session)):
    return await auth_service.reset_password_with_token(request, db)