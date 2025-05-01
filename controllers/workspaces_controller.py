from fastapi import APIRouter, Depends
from sqlmodel import Session
from services.workspaces_service import WorkspacesService
from databases.dependencies import get_session
from models.requests.share_request import ShareRequest

router = APIRouter(prefix = "/api/workspaces")

@router.post("/share")
async def share(request: ShareRequest, db: Session = Depends(get_session)):
    workspaces_service = WorkspacesService(db)
    return await workspaces_service.share(request)