from sqlmodel import Field, Relationship
from timestamp_mixin import TimestampMixin
from lt_role import LtRole
from ms_user_permission import MsUserPermission
from tr_workspace import TrWorkspace
import uuid

class MsUser(TimestampMixin, table = True):
    userID: uuid.UUID = Field(default_factory = uuid.uuid4, primary_key = True)
    name: str = Field(max_length = 255)
    email: str = Field(max_length = 255)
    password: str = Field(max_length = 64)
    roleID: int = Field(foreign_key = "LtRole.roleID")
    isVerified: bool

    role: LtRole = Relationship(back_populates = "users")
    userPermissions: list["MsUserPermission"] = Relationship(back_populates = "user")
    workspaces: list["TrWorkspace"] = Relationship(back_populates = "user")