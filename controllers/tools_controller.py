from fastapi import APIRouter, Depends
from sqlmodel import Session
from services.tools_service import ToolsService
from databases.dependencies import get_session
from models.requests.transcript_request import TranscriptRequest
from models.requests.summarize_request import SummarizeRequest
from models.requests.share_request import ShareRequest

router = APIRouter(prefix = "/api/tools")

@router.post("/transcript")
async def transcript(request: TranscriptRequest, db: Session = Depends(get_session)):
    tools_service = ToolsService(db)
    return await tools_service.transcript(request)

@router.post("/summarize")
async def summarize(request: SummarizeRequest, db: Session = Depends(get_session)):
    tools_service = ToolsService(db)
    return await tools_service.summarize(request)

@router.post("/share")
async def share(request: ShareRequest, db: Session = Depends(get_session)):
    tools_service = ToolsService(db)
    return await tools_service.share(request)