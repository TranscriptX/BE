from sqlmodel import Field, Relationship
from timestamp_mixin import TimestampMixin
from tr_verification_token import TrVerificationToken

class LtVerificationType(TimestampMixin, table = True):
    verificationTypeID: int = Field(default = None, primary_key = True)
    type: str = Field(max_length = 36)

    tokens: list["TrVerificationToken"] = Relationship(back_populates = "verificationType")