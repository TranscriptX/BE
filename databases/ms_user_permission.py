from sqlmodel import Field, Relationship
from timestamp_mixin import TimestampMixin
from lt_feature import LtFeature
from ms_user import MsUser
import uuid

class MsUserPermission(TimestampMixin, table = True):
    userPermissionID: uuid.UUID = Field(default_factory = uuid.uuid4, primary_key = True)
    userID: int = Field(foreign_key = "MsUser.userID")
    featureID: int = Field(foreign_key = "LtFeature.featureID")

    user: MsUser = Relationship(back_populates = "userPermissions")
    feature: LtFeature = Relationship(back_populates = "userPermissions")