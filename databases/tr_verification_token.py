from sqlmodel import Field, Relationship
from timestamp_mixin import TimestampMixin
from datetime import datetime
from lt_verification_type import LtVerificationType

class TrVerificationToken(TimestampMixin, table = True):
    verificationTokenID: int = Field(default = None, primary_key = True)
    token: str = Field(sa_column_kwargs = {"type": "TEXT"})
    expires: datetime
    verificationTypeID: int = Field(foreign_key = "LtVerificationType.verificationTypeID")

    verificationType: LtVerificationType = Relationship(back_populates = "tokens")