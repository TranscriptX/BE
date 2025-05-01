from fastapi import FastAPI
from pipelines.summarization_pipeline import model, tokenizer
from pipelines.transcription_pipeline import model, processor
from databases.database import create_db_and_tables
from controllers.tools_controller import router as tools_router
from controllers import auth_controller

app = FastAPI(max_request_size = 256 * 1024 * 1024)
# app.include_router(tools_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_controller.router)