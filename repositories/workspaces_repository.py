from sqlmodel import Session, select
from databases.tr_workspace import TrWorkspace
from databases.tr_workspace_detail import TrWorkspaceDetail
from models.requests.share_request import ShareRequest
from models.requests.get_workspace_detail_request import GetWorkspaceDetailRequest
from models.responses.response import Response
from models.responses.share_response import ShareResult
from models.responses.get_workspace_detail_response import GetWorkspaceDetailResult
from utils.base64_utils import get_file_extension
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
        
    async def getDetail(self, request: GetWorkspaceDetailRequest):
        try:
            workspace = self.db.exec(
                select(TrWorkspace).where(TrWorkspace.workspaceID == request.workspaceID)
            ).first()

            if workspace is None:
                return Response(
                    statusCode = HTTPStatus.NOT_FOUND,
                    message = "Workspace not found",
                    payload = None
                )
            
            if workspace.userID != request.userID and workspace.link is None:
                return Response(
                    statusCode = HTTPStatus.NOT_FOUND,
                    message = "Workspace not found",
                    payload = None
                )

            transcription = None
            summarization = None 
            for wd in workspace.workspaceDetail:
                if wd.toolsID == 1:
                    summarization = wd.result
                elif wd.toolsID == 2:
                    transcription = wd.result

            type = None
            if transcription is None and summarization is not None:
                type = "Summarization"
            elif transcription is not None and summarization is None:
                type = "Transcription"
            elif transcription is not None and summarization is not None:
                type = "Transcription and Summarization"
            else:
                return Response(
                    statusCode = HTTPStatus.INTERNAL_SERVER_ERROR,
                    message = "Workspace error",
                    payload = None
                )

            payload = GetWorkspaceDetailResult(
                title = workspace.name,
                author = workspace.user.name,
                createdDate = workspace.dateIn,
                type = type,
                fileName = f"{request.workspaceID}{get_file_extension(workspace.file)}",
                file = workspace.file,
                sharedLink = workspace.link,
                description = workspace.description,
                transcription = transcription,
                summarization = summarization,
                isShareable = (workspace.link == None),
                isCanSummarized = (transcription is not None and summarization is None)
            )

            if workspace.userID != request.userID:
                payload.isShareable = False
                payload.isCanSummarized = False

            return Response[GetWorkspaceDetailResult](
                statusCode = HTTPStatus.OK,
                message = None,
                payload = payload
            )
        except Exception as e:
            return Response(
                statusCode = HTTPStatus.INTERNAL_SERVER_ERROR,
                message = str(e),
                payload = None
            )