from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models.modification import Modification
from app.models.contract import Contract
from app.models.user import User
from app.models.version import Version
from app.models.audit_log import AuditLog

from app.schemas.modification import (
    ModificationCreate,
    ModificationDecision,
    ModificationResponse
)

from app.auth import (
    require_any_role,
    require_role
)


router = APIRouter(
    prefix="/modifications",
    tags=["Modifications"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# CREATE MODIFICATION REQUEST
# USER / ADMIN / APPROVAL
# --------------------------------------------------

@router.post(
    "/",
    response_model=ModificationResponse
)
def create_modification(
    modification_data: ModificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval",
            "Reviewer"
        )
    )
):

    # Check contract
    contract = db.query(Contract).filter(
        Contract.id == modification_data.contract_id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    # Create modification request
    new_modification = Modification(
        original_value=modification_data.original_value,
        proposed_value=modification_data.proposed_value,
        modification_reason=modification_data.modification_reason,
        contract_id=modification_data.contract_id,
        modified_by=current_user.id,
        status="PENDING"
    )

    db.add(new_modification)
    db.commit()
    db.refresh(new_modification)

    return new_modification


# --------------------------------------------------
# VIEW ALL MODIFICATIONS
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[ModificationResponse]
)
def get_modifications(
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

    modifications = db.query(
        Modification
    ).all()

    return modifications


# --------------------------------------------------
# VIEW MY MODIFICATION REQUESTS
# --------------------------------------------------

@router.get(
    "/my-requests",
    response_model=list[ModificationResponse]
)
def get_my_modification_requests(
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

    modifications = db.query(
        Modification
    ).filter(
        Modification.modified_by == current_user.id
    ).all()

    return modifications


# --------------------------------------------------
# VIEW PENDING REQUESTS
# APPROVER ONLY
# --------------------------------------------------

@router.get(
    "/pending",
    response_model=list[ModificationResponse]
)
def get_pending_modifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("Approval")
    )
):

    modifications = db.query(
        Modification
    ).filter(
        Modification.status == "PENDING"
    ).all()

    return modifications


# --------------------------------------------------
# VIEW SINGLE MODIFICATION
# --------------------------------------------------

@router.get(
    "/{modification_id}",
    response_model=ModificationResponse
)
def get_modification(
    modification_id: int,
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

    modification = db.query(
        Modification
    ).filter(
        Modification.id == modification_id
    ).first()

    if not modification:
        raise HTTPException(
            status_code=404,
            detail="Modification not found"
        )

    return modification


# --------------------------------------------------
# APPROVE / REJECT MODIFICATION
# APPROVER ONLY
# --------------------------------------------------
@router.put(
    "/{modification_id}/decision",
    response_model=ModificationResponse
)
def decide_modification(
    modification_id: int,
    decision_data: ModificationDecision,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("Approval")
    )
):

    modification = db.query(
        Modification
    ).filter(
        Modification.id == modification_id
    ).first()

    if not modification:
        raise HTTPException(
            status_code=404,
            detail="Modification not found"
        )

    # Request must be PENDING
    if modification.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Modification request has already been processed"
        )

    # REJECTED request must have rejection reason
    if (
        decision_data.status == "REJECTED"
        and not decision_data.rejection_reason
    ):
        raise HTTPException(
            status_code=400,
            detail="Rejection reason is required"
        )

    # APPROVED
    if decision_data.status == "APPROVED":

        modification.status = "APPROVED"

        modification.approver_comments = (
            decision_data.approver_comments
        )

        modification.rejection_reason = None

        # Get latest version number
        latest_version = db.query(
            Version
        ).filter(
            Version.contract_id == modification.contract_id
        ).order_by(
            Version.version_number.desc()
        ).first()

        if latest_version:
            new_version_number = (
                latest_version.version_number + 1
            )
        else:
            new_version_number = 1

        # Create new contract version
        new_version = Version(
            version_number=new_version_number,
            file_path=None,
            changes=(
                "Modification approved. "
                "Original: "
                + modification.original_value
                + " | Proposed: "
                + modification.proposed_value
            ),
            contract_id=modification.contract_id,
            created_by=current_user.id
        )

        db.add(new_version)

        # Create audit log for version creation
        audit_log = AuditLog(
            action="VERSION_CREATED",
            description=(
                "Version "
                + str(new_version_number)
                + " created for Contract "
                + str(modification.contract_id)
                + " after Modification "
                + str(modification.id)
                + " was approved."
            ),
            user_id=current_user.id
        )

        db.add(audit_log)

    # REJECTED
    elif decision_data.status == "REJECTED":

        modification.status = "REJECTED"

        modification.approver_comments = (
            decision_data.approver_comments
        )

        modification.rejection_reason = (
            decision_data.rejection_reason
        )

        # Create audit log for rejection
        audit_log = AuditLog(
            action="MODIFICATION_REJECTED",
            description=(
                "Modification "
                + str(modification.id)
                + " was rejected for Contract "
                + str(modification.contract_id)
                + "."
            ),
            user_id=current_user.id
        )

        db.add(audit_log)

    modification.approved_by = current_user.id

    modification.decision_date = datetime.now()

    db.commit()
    db.refresh(modification)

    return modification














# @router.put(
#     "/{modification_id}/decision",
#     response_model=ModificationResponse
# )
# def decide_modification(
#     modification_id: int,
#     decision_data: ModificationDecision,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_role("Approval")
#     )
# ):

#     modification = db.query(
#         Modification
#     ).filter(
#         Modification.id == modification_id
#     ).first()

#     if not modification:
#         raise HTTPException(
#             status_code=404,
#             detail="Modification not found"
#         )

#     # Request must be PENDING
#     if modification.status != "PENDING":
#         raise HTTPException(
#             status_code=400,
#             detail="Modification request has already been processed"
#         )

#     # REJECTED request must have rejection reason
#     if (
#         decision_data.status == "REJECTED"
#         and not decision_data.rejection_reason
#     ):
#         raise HTTPException(
#             status_code=400,
#             detail="Rejection reason is required"
#         )

#     # APPROVED
#     if decision_data.status == "APPROVED":

#         modification.status = "APPROVED"

#         modification.approver_comments = (
#             decision_data.approver_comments
#         )

#         modification.rejection_reason = None

#     # REJECTED
#     elif decision_data.status == "REJECTED":

#         modification.status = "REJECTED"

#         modification.approver_comments = (
#             decision_data.approver_comments
#         )

#         modification.rejection_reason = (
#             decision_data.rejection_reason
#         )

#     modification.approved_by = current_user.id

#     modification.decision_date = datetime.now()

#     db.commit()
#     db.refresh(modification)

#     return modification






























































# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database import SessionLocal
# from app.models.modification import Modification
# from app.models.contract import Contract
# from app.models.user import User

# from app.schemas.modification import (
#     ModificationCreate,
#     ModificationResponse
# )

# from app.auth import require_any_role


# router = APIRouter(
#     prefix="/modifications",
#     tags=["Modifications"]
# )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # Create Modification
# @router.post("/", response_model=ModificationResponse)
# def create_modification(
#     modification_data: ModificationCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_any_role(
#             "Admin",
#             "Approval"
#         )
#     )
# ):
#     contract = db.query(Contract).filter(
#         Contract.id == modification_data.contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     new_modification = Modification(
#         modification_text=modification_data.modification_text,
#         contract_id=modification_data.contract_id,
#         modified_by=current_user.id
#     )

#     db.add(new_modification)
#     db.commit()
#     db.refresh(new_modification)

#     return new_modification


# # Get All Modifications
# @router.get("/", response_model=list[ModificationResponse])
# def get_modifications(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_any_role(
#             "Admin",
#             "Approval",
#             "Reviewer",
#             "Role Management"
#         )
#     )
# ):
#     modifications = db.query(Modification).all()

#     return modifications


# # Get Modifications by Contract
# @router.get(
#     "/contract/{contract_id}",
#     response_model=list[ModificationResponse]
# )
# def get_modifications_by_contract(
#     contract_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_any_role(
#             "Admin",
#             "Approval",
#             "Reviewer",
#             "Role Management"
#         )
#     )
# ):
#     contract = db.query(Contract).filter(
#         Contract.id == contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     modifications = db.query(Modification).filter(
#         Modification.contract_id == contract_id
#     ).all()

#     return modifications


# # Get Single Modification
# @router.get(
#     "/{modification_id}",
#     response_model=ModificationResponse
# )
# def get_modification(
#     modification_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_any_role(
#             "Admin",
#             "Approval",
#             "Reviewer",
#             "Role Management"
#         )
#     )
# ):
#     modification = db.query(Modification).filter(
#         Modification.id == modification_id
#     ).first()

#     if not modification:
#         raise HTTPException(
#             status_code=404,
#             detail="Modification not found"
#         )

#     return modification


# # Delete Modification
# @router.delete("/{modification_id}")
# def delete_modification(
#     modification_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_any_role("Admin")
#     )
# ):
#     modification = db.query(Modification).filter(
#         Modification.id == modification_id
#     ).first()

#     if not modification:
#         raise HTTPException(
#             status_code=404,
#             detail="Modification not found"
#         )

#     db.delete(modification)
#     db.commit()

#     return {
#         "message": "Modification deleted successfully"
#     }