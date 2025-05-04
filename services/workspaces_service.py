from repositories.workspaces_repository import WorkspacesRepository
from sqlmodel import Session
from models.requests.share_request import ShareRequest
from models.requests.get_workspace_detail_request import GetWorkspaceDetailRequest
from models.requests.export_workspace_request import ExportWorkspaceRequest
from models.responses.response import Response
from models.requests.dashboard_request import DashboardFilterRequest
from http import HTTPStatus
import os

class WorkspacesService:
    def __init__(self, db: Session):
        self.db = db
        self.workspace_repository = WorkspacesRepository(db)

    async def share(self, request: ShareRequest):
        return await self.workspace_repository.share(request)
    
    async def getDetail(self, request: GetWorkspaceDetailRequest):
        return await self.workspace_repository.getDetail(request)
    
    async def export(self, request: ExportWorkspaceRequest):
        return await self.workspace_repository.export(request)
    
    async def getDashboard(self, request: DashboardFilterRequest):
        return await self.workspace_repository.getDashboard(request)