from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class ModificationCreate(BaseModel):
    original_value: str
    proposed_value: str
    modification_reason: str | None = None
    contract_id: int


class ModificationDecision(BaseModel):
    status: Literal["APPROVED", "REJECTED"]
    approver_comments: str | None = None
    rejection_reason: str | None = None


class ModificationResponse(BaseModel):
    id: int
    original_value: str
    proposed_value: str
    modification_reason: str | None = None
    contract_id: int
    modified_by: int
    request_date: datetime
    status: str
    approver_comments: str | None = None
    rejection_reason: str | None = None
    approved_by: int | None = None
    decision_date: datetime | None = None

    class Config:
        from_attributes = True

























# from pydantic import BaseModel


# class ModificationCreate(BaseModel):
#     modification_text: str
#     contract_id: int


# class ModificationResponse(BaseModel):
#     id: int
#     modification_text: str
#     contract_id: int
#     modified_by: int

#     class Config:
#         from_attributes = True