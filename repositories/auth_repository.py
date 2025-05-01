from sqlalchemy.orm import Session
from databases.ms_user import MsUser

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(MsUser).filter(MsUser.email == email).first()

    def create_user(self, user: MsUser):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: MsUser):
        self.db.commit()
        self.db.refresh(user)
        return user
