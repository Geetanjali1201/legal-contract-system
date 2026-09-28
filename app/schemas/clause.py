from pydantic import BaseModel


class ClauseCreate(BaseModel):
    clause_text: str
    contract_id: int


class ClauseUpdate(BaseModel):
    clause_text: str


class ClauseResponse(BaseModel):
    id: int
    clause_text: str
    contract_id: int

    class Config:
        from_attributes = True