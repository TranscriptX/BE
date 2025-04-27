from sqlmodel import Field, Relationship
from timestamp_mixin import TimestampMixin
from ms_user import MsUser

class LtRole(TimestampMixin, table = True):
    roleID: int = Field(default = None, primary_key = True)
    name: str = Field(max_length = 36)

    users: list["MsUser"] = Relationship(back_populates = "role")