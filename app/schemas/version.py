from pydantic import BaseModel


class VersionCreate(BaseModel):
    version_number: int
    file_path: str | None = None
    changes: str | None = None
    contract_id: int


class VersionResponse(BaseModel):
    id: int
    version_number: int
    file_path: str | None = None
    changes: str | None = None
    contract_id: int
    created_by: int

    class Config:
        from_attributes = True