from sqlmodel import SQLModel, Session
from databases.database import engine
from databases.lt_tools import LtTools

def seed_database():
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

        session.add_all(tools)
        session.commit()
        print("Successfully seed database")

if __name__ == "__main__":
    seed_database()