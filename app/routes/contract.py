from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractResponse

from app.auth import require_any_role
from app.models.user import User


router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Contract
# Allowed: Admin, Approval
@router.post("/", response_model=ContractResponse)
def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Approval")
    )
):
    new_contract = Contract(
        title=contract.title,
        description=contract.description,
        status=contract.status,
        start_date=contract.start_date,
        end_date=contract.end_date
    )

    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)

    return new_contract


# Get All Contracts + Search + Filter
# Allowed: Admin, Approval, Reviewer, Role Management
@router.get("/", response_model=list[ContractResponse])
def get_contracts(
    search: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval",
            "Reviewer",
            "Role Management"
        )
    )
):
    query = db.query(Contract)

    # Search by contract title
    if search:
        query = query.filter(
            Contract.title.ilike(f"%{search}%")
        )

    # Filter by contract status
    if status:
        query = query.filter(
            Contract.status == status
        )

    return query.all()


# Get Contract by ID
# Allowed: Admin, Approval, Reviewer, Role Management
@router.get("/{contract_id}", response_model=ContractResponse)
def get_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval",
            "Reviewer",
            "Role Management"
        )
    )
):
    contract = db.query(Contract).filter(
        Contract.id == contract_id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    return contract


# Update Contract
# Allowed: Admin, Approval
@router.put("/{contract_id}", response_model=ContractResponse)
def update_contract(
    contract_id: int,
    contract_data: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Approval")
    )
):
    contract = db.query(Contract).filter(
        Contract.id == contract_id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    contract.title = contract_data.title
    contract.description = contract_data.description
    contract.status = contract_data.status
    contract.start_date = contract_data.start_date
    contract.end_date = contract_data.end_date

    db.commit()
    db.refresh(contract)

    return contract


# Delete Contract
# Allowed: Admin only
@router.delete("/{contract_id}")
def delete_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin")
    )
):
    contract = db.query(Contract).filter(
        Contract.id == contract_id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    db.delete(contract)
    db.commit()

    return {
        "message": "Contract deleted successfully"
    }



























# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session

# from app.database import SessionLocal
# from app.models.contract import Contract
# from app.schemas.contract import ContractCreate, ContractResponse


# router = APIRouter(
#     prefix="/contracts",
#     tags=["Contracts"]
# )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # Create Contract
# @router.post("/", response_model=ContractResponse)
# def create_contract(
#     contract: ContractCreate,
#     db: Session = Depends(get_db)
# ):
#     new_contract = Contract(
#         title=contract.title,
#         description=contract.description,
#         status=contract.status,
#         start_date=contract.start_date,
#         end_date=contract.end_date
#     )

#     db.add(new_contract)
#     db.commit()
#     db.refresh(new_contract)

#     return new_contract


# # Get All Contracts + Search + Filter
# @router.get("/", response_model=list[ContractResponse])
# def get_contracts(
#     search: str | None = Query(default=None),
#     status: str | None = Query(default=None),
#     db: Session = Depends(get_db)
# ):
#     query = db.query(Contract)

#     # Search by contract title
#     if search:
#         query = query.filter(
#             Contract.title.ilike(f"%{search}%")
#         )

#     # Filter by contract status
#     if status:
#         query = query.filter(
#             Contract.status == status
#         )

#     return query.all()


# # Get Contract by ID
# @router.get("/{contract_id}", response_model=ContractResponse)
# def get_contract(
#     contract_id: int,
#     db: Session = Depends(get_db)
# ):
#     contract = db.query(Contract).filter(
#         Contract.id == contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     return contract


# # Update Contract
# @router.put("/{contract_id}", response_model=ContractResponse)
# def update_contract(
#     contract_id: int,
#     contract_data: ContractCreate,
#     db: Session = Depends(get_db)
# ):
#     contract = db.query(Contract).filter(
#         Contract.id == contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     contract.title = contract_data.title
#     contract.description = contract_data.description
#     contract.status = contract_data.status
#     contract.start_date = contract_data.start_date
#     contract.end_date = contract_data.end_date

#     db.commit()
#     db.refresh(contract)

#     return contract


# # Delete Contract
# @router.delete("/{contract_id}")
# def delete_contract(
#     contract_id: int,
#     db: Session = Depends(get_db)
# ):
#     contract = db.query(Contract).filter(
#         Contract.id == contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     db.delete(contract)
#     db.commit()

#     return {
#         "message": "Contract deleted successfully"
#     }














# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database import SessionLocal
# from app.models.contract import Contract
# from app.schemas.contract import ContractCreate, ContractResponse


# router = APIRouter(
#     prefix="/contracts",
#     tags=["Contracts"]
# )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # Create Contract
# @router.post("/", response_model=ContractResponse)
# def create_contract(
#     contract: ContractCreate,
#     db: Session = Depends(get_db)
# ):
#     new_contract = Contract(
#         title=contract.title,
#         description=contract.description,
#         status=contract.status,
#         start_date=contract.start_date,
#         end_date=contract.end_date
#     )

#     db.add(new_contract)
#     db.commit()
#     db.refresh(new_contract)

#     return new_contract


# # Get All Contracts
# @router.get("/", response_model=list[ContractResponse])
# def get_contracts(db: Session = Depends(get_db)):
#     contracts = db.query(Contract).all()
#     return contracts


# # Get Contract by ID
# @router.get("/{contract_id}", response_model=ContractResponse)
# def get_contract(
#     contract_id: int,
#     db: Session = Depends(get_db)
# ):
#     contract = db.query(Contract).filter(
#         Contract.id == contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     return contract


# # Update Contract
# @router.put("/{contract_id}", response_model=ContractResponse)
# def update_contract(
#     contract_id: int,
#     contract_data: ContractCreate,
#     db: Session = Depends(get_db)
# ):
#     contract = db.query(Contract).filter(
#         Contract.id == contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     contract.title = contract_data.title
#     contract.description = contract_data.description
#     contract.status = contract_data.status
#     contract.start_date = contract_data.start_date
#     contract.end_date = contract_data.end_date

#     db.commit()
#     db.refresh(contract)

#     return contract


# # Delete Contract
# @router.delete("/{contract_id}")
# def delete_contract(
#     contract_id: int,
#     db: Session = Depends(get_db)
# ):
#     contract = db.query(Contract).filter(
#         Contract.id == contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     db.delete(contract)
#     db.commit()

#     return {
#         "message": "Contract deleted successfully"
#     }