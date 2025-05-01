from repositories.workspaces_repository import WorkspacesRepository
from sqlmodel import Session
from models.requests.share_request import ShareRequest
from models.responses.response import Response
from http import HTTPStatus
import os

class WorkspacesService:
    def __init__(self, db: Session):
        self.db = db
        self.workspace_repository = WorkspacesRepository(db)

    async def share(self, request: ShareRequest):
        return await self.workspace_repository.share(request)