



from pydantic import BaseModel
from datetime import date
from typing import Literal


class ContractBase(BaseModel):

    title: str

    description: str | None = None

    status: Literal[
        "Draft",
        "Active",
        "Expired",
        "Terminated"
    ] = "Draft"

    start_date: date | None = None

    end_date: date | None = None


class ContractCreate(ContractBase):
    pass


class ContractResponse(ContractBase):

    id: int

    class Config:
        from_attributes = True











# from pydantic import BaseModel
# from datetime import date


# class ContractBase(BaseModel):
#     title: str
#     description: str | None = None
#     status: str = "Draft"
#     start_date: date | None = None
#     end_date: date | None = None


# class ContractCreate(ContractBase):
#     pass


# class ContractResponse(ContractBase):
#     id: int

#     class Config:
#         from_attributes = True