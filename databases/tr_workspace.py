from sqlmodel import Field, Relationship
from timestamp_mixin import TimestampMixin
from ms_user import MsUser
from tr_workspace_detail import TrWorkspaceDetail
import uuid

class TrWorkspace(TimestampMixin, table = True):
    workspaceID: uuid.UUID = Field(default_factory = uuid.uuid4, primary_key = True)
    name: str | None = Field(max_length = 255)
    description: str | None = Field(sa_column_kwargs = {"type": "TEXT"})
    userID: str = Field(foreign_key = "MsUser.roleID", max_length = 36)
    file: str = Field(sa_column_kwargs = {"type": "TEXT"})

    user: MsUser = Relationship(back_populates = "workspaces")
    workspaceDetail: list["TrWorkspaceDetail"] = Relationship(back_populates = "workspace")