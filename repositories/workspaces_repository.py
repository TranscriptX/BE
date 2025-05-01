from sqlmodel import Session, select
from databases.tr_workspace import TrWorkspace
from databases.tr_workspace_detail import TrWorkspaceDetail
from models.requests.share_request import ShareRequest
from models.responses.response import Response
from models.responses.share_response import ShareResult
from http import HTTPStatus
from dotenv import load_dotenv
import uuid
import os

class WorkspacesRepository:
    def __init__(self, db: Session):
        load_dotenv()
        self.db = db
        self.client_url = os.getenv("CLIENT_URL")

    async def share(self, request: ShareRequest):
        try:
            workspace = self.db.exec(
                select(TrWorkspace).where(TrWorkspace.workspaceID == request.workspaceID)
            ).first()

            if workspace is None:
                return Response(
                    statusCode = HTTPStatus.BAD_REQUEST,
                    message = str(e),
                    payload = None 
                )
            
            if request.isGrantAccess:
                workspace.link = f"{self.client_url}/workspace/{workspace.workspaceID}"
            else:
                workspace.link = None


            self.db.commit()

            return Response[ShareResult](
                statusCode = HTTPStatus.CREATED,
                message = None,
                payload = ShareResult(
                    link = workspace.link
                )
            ) 
        except Exception as e:
            return Response(
                statusCode = HTTPStatus.INTERNAL_SERVER_ERROR,
                message = str(e),
                payload = None
            )