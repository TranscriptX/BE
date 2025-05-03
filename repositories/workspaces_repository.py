from sqlmodel import Session, select
from databases.tr_workspace import TrWorkspace
from databases.tr_workspace_detail import TrWorkspaceDetail
from models.requests.share_request import ShareRequest
from models.requests.get_workspace_detail_request import GetWorkspaceDetailRequest
from models.requests.export_workspace_request import ExportWorkspaceRequest
from models.responses.response import Response
from models.responses.share_response import ShareResult
from models.responses.get_workspace_detail_response import GetWorkspaceDetailResult
from utils.base64_utils import get_file_extension
from fastapi.responses import StreamingResponse
from http import HTTPStatus
from dotenv import load_dotenv
from xhtml2pdf import pisa
from io import BytesIO
import uuid
import os
import asyncio
import traceback

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
                    statusCode = HTTPStatus.NOT_FOUND,
                    message = "Workspace is not found",
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
        
    async def export(self, request: ExportWorkspaceRequest):
        try:
            workspace = self.db.exec(
                select(TrWorkspace).where(TrWorkspace.workspaceID == request.workspaceID)
            ).first()

            if workspace is None:
                return Response(
                    statusCode = HTTPStatus.NOT_FOUND,
                    message = "Workspace is not found",
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
                                
            html_template = """
                <html>
                    <head>
                        <style>
                            @page {
                                size: A4 portrait;
                                margin: 2cm;
                            }
                        
                            body {
                                font-family: "Times New Roman", Times, serif;
                            }
                            
                            #workspace-title {
                                text-align: center;
                            }
                            
                            table {
                                margin-top: 3rem;
                                margin-bottom: 3rem;
                                width: 100%;
                            }
                            
                            
                            .container {
                                background-color: #f1f5f9;
                                margin-top: 0rem; 
                                padding-top: 0.25rem;
                                padding-bottom: 0.25rem;
                                padding-left: 0.5rem;
                                padding-right: 0.5rem;
                                width: 100%;
                            }
                            
                            .container p {
                                text-align: justified;
                                width: 100%;
                                white-space: normal;
                            }
                            
                            .mb-0 {
                                margin-bottom: 0rem;
                            }
                        </style>
                    </head>
                    <body>
                        <h1 id="workspace-title">[[WORKSPACE_TITLE]]</h1>

                        <table>
                            <thead>
                                
                            </thead>
                            <tbody>
                                <tr>
                                    <td width="20%"> Author </td>
                                    <td width="80%"> : [[AUTHOR]] </td>
                                </tr>
                                <tr>
                                    <td> Created Date </td>
                                    <td> : [[CREATED_DATE]] </td>
                                </tr>  
                                <tr>
                                    <td> Type </td>
                                    <td> : [[TYPE]] </td>
                                </tr>  
                                <tr>
                                    <td> Link </td>
                                    <td> : [[LINK]] </td>
                                </tr>      
                                <tr>
                                    <td> Description </td>
                                    <td> : [[DESCRIPTION]] </td>
                                </tr>
                            </tbody>
                        </table>       
                        
                        <p class="mb-0"> Transcription: </p>
                        <div class="container">
                            <p> [[TRANSCRIPTION]] </p>
                        </div>
                        
                        <p class="mb-0"> Summary: </p>
                        <div class="container">
                            <p> [[SUMMARY]] </p>
                        </div>                        
                    </body>
                </html>             
            """

            html_template = html_template \
                .replace("[[WORKSPACE_TITLE]]", workspace.name if workspace.name is not None else f"{workspace.user.name}'s Workspace") \
                .replace("[[AUTHOR]]", workspace.user.name) \
                .replace("[[CREATED_DATE]]", workspace.dateIn.strftime("%Y-%m-%d")) \
                .replace("[[TYPE]]", type) \
                .replace("[[LINK]]", workspace.link if workspace.link is not None else "-") \
                .replace("[[DESCRIPTION]]", workspace.description if workspace.description is not None else "-") \
                .replace("[[TRANSCRIPTION]]", transcription if transcription is not None else "-") \
                .replace("[[SUMMARY]]", summarization if summarization is not None else "-")
        
            pdf_io = BytesIO()          

            pisa_status = pisa.CreatePDF(html_template, dest = pdf_io)

            if pisa_status.err:
                return Response(
                    statusCode = HTTPStatus.INTERNAL_SERVER_ERROR,
                    message = "Error when generating PDF",
                    payload = None
                )

            pdf_io.seek(0)

            print(pdf_io)

            return StreamingResponse(
                pdf_io,
                media_type = "application/pdf",
                headers = {"Content-Disposition": f"attachment; filename={workspace.workspaceID}.pdf"}
            )
        except Exception as e:
            return Response(
                statusCode = HTTPStatus.INTERNAL_SERVER_ERROR,
                message = str(traceback.format_exc()),
                payload = None
            )