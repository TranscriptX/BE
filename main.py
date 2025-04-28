from fastapi import FastAPI, Depends
from sqlmodel import Session, select

from databases.database import engine, create_db_and_tables
from databases.dependencies import get_session
from databases.lt_role import LtRole

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/roles/")
def get_roles(session: Session = Depends(get_session)):
    roles = session.exec(select(LtRole)).all()
    return roles