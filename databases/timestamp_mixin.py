from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class TimestampMixin(SQLModel):
    dateIn: datetime = Field(default_factory = timezone.utc)
    dateUp: datetime = Field(default_factory = timezone.utc)
    isActive: bool = Field(default = True)