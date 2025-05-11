from typing import List
from pydantic import BaseModel, Field

class DeleteRequest(BaseModel):
    workspaceID: List[int] = Field(..., alias="workspaceID")