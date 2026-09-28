from pydantic import BaseModel
from typing import Literal


class ApprovalCreate(BaseModel):
    contract_id: int
    comments: str | None = None


class ApprovalUpdate(BaseModel):
    status: Literal[
        "Pending",
        "Approved",
        "Rejected"
    ]
    comments: str | None = None


class ApprovalResponse(BaseModel):
    id: int
    status: str
    comments: str | None = None
    contract_id: int
    approved_by: int | None = None

    class Config:
        from_attributes = True