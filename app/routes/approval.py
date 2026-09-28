from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.approval import Approval
from app.models.contract import Contract
from app.models.user import User

from app.schemas.approval import (
    ApprovalCreate,
    ApprovalUpdate,
    ApprovalResponse
)

from app.auth import (
    require_any_role,
    require_role
)


router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# Create Approval Request
# Allowed: Admin, Approval
# =========================================================

@router.post(
    "/",
    response_model=ApprovalResponse
)
def create_approval(
    approval_data: ApprovalCreate,
    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval"
        )
    )
):

    # Check contract
    contract = db.query(Contract).filter(
        Contract.id == approval_data.contract_id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    # Check whether pending approval already exists
    existing_approval = db.query(Approval).filter(
        Approval.contract_id == approval_data.contract_id,
        Approval.status == "Pending"
    ).first()

    if existing_approval:
        raise HTTPException(
            status_code=400,
            detail="Approval request already exists for this contract"
        )

    new_approval = Approval(
        status="Pending",
        comments=approval_data.comments,
        contract_id=approval_data.contract_id,
        approved_by=None
    )

    db.add(new_approval)
    db.commit()
    db.refresh(new_approval)

    return new_approval


# =========================================================
# Get All Approvals
# Allowed: Admin, Approval, Reviewer, Role Management
# =========================================================

@router.get(
    "/",
    response_model=list[ApprovalResponse]
)
def get_approvals(
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

    approvals = db.query(Approval).all()

    return approvals


# =========================================================
# Get Approval by ID
# Allowed: Admin, Approval, Reviewer, Role Management
# =========================================================

@router.get(
    "/{approval_id}",
    response_model=ApprovalResponse
)
def get_approval(
    approval_id: int,
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

    approval = db.query(Approval).filter(
        Approval.id == approval_id
    ).first()

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    return approval


# =========================================================
# Approve / Reject Contract
# Allowed: Admin, Approval
# =========================================================

@router.put(
    "/{approval_id}",
    response_model=ApprovalResponse
)
def update_approval(
    approval_id: int,
    approval_data: ApprovalUpdate,
    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval"
        )
    )
):

    approval = db.query(Approval).filter(
        Approval.id == approval_id
    ).first()

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval not found"
        )

    # Already processed
    if approval.status != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Approval has already been processed"
        )

    approval.status = approval_data.status
    approval.comments = approval_data.comments
    approval.approved_by = current_user.id

    # Update contract status
    contract = db.query(Contract).filter(
        Contract.id == approval.contract_id
    ).first()

    if contract:

        if approval_data.status == "Approved":
            contract.status = "Active"

        elif approval_data.status == "Rejected":
            contract.status = "Draft"

    db.commit()
    db.refresh(approval)

    return approval