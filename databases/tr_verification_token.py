from sqlmodel import Field, Relationship, Text
from databases.timestamp_mixin import TimestampMixin
from datetime import datetime
# from databases.lt_verification_type import LtVerificationType

class TrVerificationToken(TimestampMixin, table = True):
    __tablename__ = "TrVerificationToken"  
    __table_args__ = {"extend_existing": True}

    verificationTokenID: int = Field(default = None, primary_key = True)
    token: str = Field(sa_column = Text)
    expires: datetime
    verificationTypeID: int = Field(foreign_key = "LtVerificationType.verificationTypeID")

    verificationType: "LtVerificationType" = Relationship(back_populates = "tokens")