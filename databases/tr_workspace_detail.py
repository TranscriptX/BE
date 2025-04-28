from sqlmodel import Field, Relationship, Text
from databases.timestamp_mixin import TimestampMixin
# from databases.lt_tools import LtTools
# from databases.tr_workspace import TrWorkspace
import uuid

class TrWorkspaceDetail(TimestampMixin, table = True):
    __tablename__ = "TrWorkspaceDetail"  
    __table_args__ = {"extend_existing": True}

    workspaceDetailID: str = Field(primary_key = True, max_length = 36)
    workspaceID: str = Field(foreign_key = "TrWorkspace.workspaceID", max_length = 36)
    toolsID: int = Field(foreign_key = "LtTools.toolsID")
    link: str | None = Field(max_length = 255)
    result: str = Field(sa_column = Text)

    tool: "LtTools" = Relationship(back_populates = "workspaceDetails")
    workspace: "TrWorkspace" = Relationship(back_populates = "workspaceDetails")