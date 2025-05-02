from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from databases.dependencies import get_session
from services.auth_service import register_user,verify_email,login_user,request_password_reset,reset_password
from models.requests.auth_requests import RegisterRequest,LoginRequest,ResetPasswordRequest,ResetPasswordTokenRequest
from models.responses.auth_responses import TokenResponse
from services import auth_service

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register")
async def register(request: RegisterRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_session)):
    return await register_user(request, background_tasks, db)

@router.get("/verify-email")
async def verify(token: str, db: Session = Depends(get_session)):
    return await verify_email(token, db)

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_session)):
    return await login_user(request, db)

@router.post("/logout")
async def logout():
    return await auth_service.logout_user()

@router.post("/request-password-reset")
async def request_reset(request: ResetPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_session)):
    return await request_password_reset(request, background_tasks, db)

@router.post("/reset-password")
async def reset_with_token(request: ResetPasswordTokenRequest, db: Session = Depends(get_session)):
    return await reset_password(request, db)