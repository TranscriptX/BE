from sqlmodel import Field, Relationship
from timestamp_mixin import TimestampMixin
from lt_tools import LtTools
from tr_workspace import TrWorkspace
import uuid

class TrWorkspaceDetail(TimestampMixin, table = True):
    workspaceDetailID: uuid.UUID = Field(default_factory = uuid.uuid4, primary_key = True)
    workspaceID: str = Field(foreign_key = "TrWorkspace.workspaceID", max_length = 36)
    toolsID: int = Field(foreign_key = "LtTools.toolsID")
    link: str | None = Field(max_length = "255")
    result: str = Field(sa_column_kwargs = {"type": "TEXT"})

    tool: LtTools = Relationship(back_populates = "workspaceDetails")
    workspace: TrWorkspace = Relationship(back_populates = "workspaceDetails")