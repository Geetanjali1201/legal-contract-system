from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.clause import Clause
from app.models.contract import Contract
from app.models.user import User

from app.schemas.clause import (
    ClauseCreate,
    ClauseUpdate,
    ClauseResponse
)

from app.auth import require_any_role


router = APIRouter(
    prefix="/clauses",
    tags=["Clauses"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================
# Create Clause
# =========================

@router.post("/", response_model=ClauseResponse)
def create_clause(
    clause_data: ClauseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval"
        )
    )
):

    contract = db.query(Contract).filter(
        Contract.id == clause_data.contract_id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    new_clause = Clause(
        clause_text=clause_data.clause_text,
        contract_id=clause_data.contract_id
    )

    db.add(new_clause)
    db.commit()
    db.refresh(new_clause)

    return new_clause


# =========================
# Get All Clauses
# =========================

@router.get("/", response_model=list[ClauseResponse])
def get_clauses(
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

    clauses = db.query(Clause).all()

    return clauses


# =========================
# Get Clauses by Contract
# =========================

@router.get(
    "/contract/{contract_id}",
    response_model=list[ClauseResponse]
)
def get_clauses_by_contract(
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

    clauses = db.query(Clause).filter(
        Clause.contract_id == contract_id
    ).all()

    return clauses


# =========================
# Get Single Clause
# =========================

@router.get(
    "/{clause_id}",
    response_model=ClauseResponse
)
def get_clause(
    clause_id: int,
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

    clause = db.query(Clause).filter(
        Clause.id == clause_id
    ).first()

    if not clause:
        raise HTTPException(
            status_code=404,
            detail="Clause not found"
        )

    return clause


# =========================
# Update Clause
# =========================

@router.put(
    "/{clause_id}",
    response_model=ClauseResponse
)
def update_clause(
    clause_id: int,
    clause_data: ClauseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval"
        )
    )
):

    clause = db.query(Clause).filter(
        Clause.id == clause_id
    ).first()

    if not clause:
        raise HTTPException(
            status_code=404,
            detail="Clause not found"
        )

    clause.clause_text = clause_data.clause_text

    db.commit()
    db.refresh(clause)

    return clause


# =========================
# Delete Clause
# =========================

@router.delete("/{clause_id}")
def delete_clause(
    clause_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role(
            "Admin"
        )
    )
):

    clause = db.query(Clause).filter(
        Clause.id == clause_id
    ).first()

    if not clause:
        raise HTTPException(
            status_code=404,
            detail="Clause not found"
        )

    db.delete(clause)
    db.commit()

    return {
        "message": "Clause deleted successfully"
    }