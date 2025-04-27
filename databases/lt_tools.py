from sqlmodel import Field, Relationship
from timestamp_mixin import TimestampMixin
from tr_workspace_detail import TrWorkspaceDetail

class LtTools(TimestampMixin, table = True):
    toolsID: int = Field(default = None, primary_key = True)
    name: str = Field(max_length = 36)

    workspaceDetail: list["TrWorkspaceDetail"] = Relationship(back_populates = "tool")