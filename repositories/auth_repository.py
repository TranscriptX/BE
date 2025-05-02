from databases.ms_user import MsUser
from databases.tr_verification_token import TrVerificationToken
from sqlalchemy.orm import Session

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(MsUser).filter(MsUser.email == email).first()

    def get_user_by_name(self, name: str):
        return self.db.query(MsUser).filter(MsUser.name == name).first()

    def create_user(self, user: MsUser):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: MsUser):
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_token(self, token: str):
        return self.db.query(TrVerificationToken).filter(TrVerificationToken.token == token).first()

    def create_verification_token(self, token: TrVerificationToken):
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def delete_verification_token(self, token: TrVerificationToken):
        self.db.delete(token)
        self.db.commit()

    def get_token_by_user(self, user_id: str, type_id: int):
        return self.db.query(TrVerificationToken).filter(
            TrVerificationToken.userID == user_id,
            TrVerificationToken.verificationTypeID == type_id
        ).first()
