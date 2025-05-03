import traceback
from fastapi import HTTPException, BackgroundTasks
from repositories.auth_repository import AuthRepository
from models.requests.auth_requests import RegisterRequest, LoginRequest, ResetPasswordRequest, ResetPasswordTokenRequest
from models.responses.auth_responses import TokenResponse
from databases.ms_user import MsUser
from databases.tr_verification_token import TrVerificationToken
from databases.lt_role import LtRole 
from utils import hash_utils, jwt_utils, email_utils
from uuid import uuid4
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

MAX_FAILED_ATTEMPTS = int(os.getenv("MAX_FAILED_ATTEMPTS", 3))
SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", 15))
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", 30))

async def register_user(request: RegisterRequest, background_tasks: BackgroundTasks, db):
        repo = AuthRepository(db)
        if repo.get_user_by_email(request.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        if repo.get_user_by_name(request.name):
            raise HTTPException(status_code=400, detail="Username already taken")

        if not hash_utils.validate_password_policy(request.password):
            raise HTTPException(status_code=400, detail="Weak password")

        hashed_password = hash_utils.hash_password(request.password)
        user_id = str(uuid4())
        verification_token = str(uuid4())


        user = MsUser(
            userID=user_id,
            name=request.name,
            email=request.email,
            password=hashed_password,
            roleID=1,
            isVerified=False
        )
        repo.create_user(user)

        token_entry = TrVerificationToken(
            verificationTokenID=str(uuid4()),
            userID=user_id,
            verificationTypeID=1,
            token=verification_token,
            expires=datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        )

        repo.create_verification_token(token_entry)
        background_tasks.add_task(email_utils.send_verification_email, request.email, verification_token)

        return {"message": "User registered, please verify your email"}

   

async def verify_email(token: str, db):
    try:
        repo = AuthRepository(db)
        token_entry = repo.get_token(token)
        if not token_entry:
            raise HTTPException(status_code=400, detail="Invalid token")

        if token_entry.expires < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Token expired")

        user = repo.get_user_by_email(token_entry.user.email)
        user.isVerified = True
        repo.update_user(user)
        repo.delete_verification_token(token_entry)

        return {"message": "Email verified successfully"}

    except Exception as e:
        traceback.print_exc()  # This will print the stack trace
        raise HTTPException(status_code=500, detail="Internal server error")

async def login_user(request: LoginRequest, db):
        repo = AuthRepository(db)
        user = repo.get_user_by_email(request.email)
        if not user or not hash_utils.verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not user.isVerified:
            raise HTTPException(status_code=403, detail="Email not verified")

        # user.failed_login_attempts = 0
        user.lastLogin = datetime.utcnow()
        repo.update_user(user)

        token = jwt_utils.create_access_token(
            data={"sub": user.userID, "role": user.roleID},
            expires_delta=timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        )

        return TokenResponse(access_token=token, token_type="bearer")
    
async def logout_user():
    return {"message": "Successfully logged out"}

async def request_password_reset(request: ResetPasswordRequest, background_tasks: BackgroundTasks, db):
        repo = AuthRepository(db)
        user = repo.get_user_by_email(request.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        token = str(uuid4())
        token_entry = TrVerificationToken(
            verificationTokenID=str(uuid4()),
            userID=user.userID,
            verificationTypeID=2,
            token=token,
            expires=datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        )
        repo.create_verification_token(token_entry)
        
        background_tasks.add_task(email_utils.send_reset_password_email, user.email, token)
        return {"message": "Reset password link sent"}

async def reset_password(request: ResetPasswordTokenRequest, db):
        repo = AuthRepository(db)
        token_entry = repo.get_token(request.token)
        if not token_entry or token_entry.verificationTypeID != 2:
            raise HTTPException(status_code=400, detail="Invalid reset token")

        if token_entry.expires < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Reset token expired")

        user = repo.get_user_by_email(token_entry.user.email)
        if not hash_utils.validate_password_policy(request.new_password):
            raise HTTPException(status_code=400, detail="Weak password")

        user.password = hash_utils.hash_password(request.new_password)
        repo.update_user(user)
        repo.delete_verification_token(token_entry)

        return {"message": "Password has been reset"}
