from typing import List, Optional
from pydantic import BaseModel

class DashboardHistoryItem(BaseModel):
    workspaceID: str
    title: str
    description: Optional[str]
    type: str  # Transcription / Summarization / Transcription and Summarization
    createdDate: str  # Format: "YYYY-MM-DD"
    fileName: str
    link: Optional[str]

class DashboardHistoryResponse(BaseModel):
    items: List[DashboardHistoryItem]
