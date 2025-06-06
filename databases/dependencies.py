from typing import Generator
from sqlmodel import Session
from databases.database import engine

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session