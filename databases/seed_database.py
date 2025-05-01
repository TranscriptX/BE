from sqlmodel import SQLModel, Session
from databases.database import engine
from databases.lt_tools import LtTools
from databases.lt_role import LtRole
from databases.ms_user import MsUser
from dotenv import load_dotenv
import uuid
import bcrypt
import os

def seed_database():
    load_dotenv()

    with Session(engine) as session:
        tools = [
            LtTools(
                toolsID = 1,
                name = "Document Summarizer"
            ),
            LtTools(
                toolsID = 2,
                name = "Video/Audio Transcription"
            )
        ]

        roles = [
            LtRole(
                roleID = 1,
                name = "User"
            ),
            LtRole(
                role = 2,
                name = "Admin"
            )
        ]

        users = [
            MsUser(
                userID = str(uuid.uuid4()),
                name = "Admin",
                email = os.getenv("ADMIN_EMAIL"),
                password = bcrypt.hashpw(os.getenv("ADMIN_PASSWORD").encode("utf-8"), bcrypt.gensalt()),
                roleID = 2,
                isVerified = True
            )
        ]

        session.add_all(tools + roles + users)
        session.commit()
        print("Successfully seed database")

if __name__ == "__main__":
    seed_database()