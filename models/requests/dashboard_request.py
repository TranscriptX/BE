from typing import Optional
from pydantic import BaseModel

class DashboardFilterRequest(BaseModel):
    userID: str
    startDate: Optional[str] = None  # Format: "YYYY-MM-DD"
    endDate: Optional[str] = None
    search: Optional[str] = None
    type: Optional[str] = None  # "Transcription", "Summarization", "Transcription and Summarization"
    sharedStatus: Optional[str] = None  # "shared" | "private"
    sortBy: Optional[str] = None  # "createdDate", "title", "description", "type", "link"
    sortOrder: Optional[str] = "desc"  # "asc" | "desc"
