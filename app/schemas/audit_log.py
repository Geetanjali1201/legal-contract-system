from pydantic import BaseModel
from datetime import datetime


class AuditLogCreate(BaseModel):
    action: str
    description: str | None = None


class AuditLogResponse(BaseModel):
    id: int
    action: str
    description: str | None = None
    user_id: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True