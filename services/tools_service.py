from repositories.tools_repository import ToolsRepository
from sqlmodel import Session
from models.requests.transcript_request import TranscriptRequest
from models.requests.summarize_request import SummarizeRequest
from models.responses.response import Response
from utils.get_file_extension import get_file_extension
from http import HTTPStatus

class ToolsService:
    def __init__(self, db: Session):
        self.db = db
        self.tools_repository = ToolsRepository(db)

    async def transcript(self, request: TranscriptRequest):
        try:
            file_extension = get_file_extension(request.file)
            if file_extension not in [".wav", ".mp3", ".mp4", ".mpeg"]:
                return Response(
                    statusCode = HTTPStatus.BAD_REQUEST,
                    message = "File must be in .wav, .mp3, .mp4, or .mpeg format",
                    payload = None
                )

            return await self.tools_repository.transcript(
                request = request, 
                file_extension = file_extension
            )
        except Exception as e:
            return Response(
                statusCode = HTTPStatus.INTERNAL_SERVER_ERROR,
                message = str(e),
                payload = None
            )
    
    async def summarize(self, request: SummarizeRequest):
        try:
            file_extension = get_file_extension(request.file)
            print(file_extension)
            if file_extension not in [".txt", ".docx", ".pdf"]:
                return Response(
                    statusCode = HTTPStatus.BAD_REQUEST,
                    message = "File must be in .txt, .docx, or .pdf format",
                    payload = None
                )

            return await self.tools_repository.summarize(
                request = request,
                file_extension = file_extension
            )
        except Exception as e:
            return Response(
                statusCode = HTTPStatus.INTERNAL_SERVER_ERROR,
                message = str(e),
                payload = None
            )