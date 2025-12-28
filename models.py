from sqlmodel import SQLModel, Field
from datetime import datetime


class ActivityLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    endpoint: str
    method: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
