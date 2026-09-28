from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate, AuditLogResponse

from app.auth import get_current_user, require_any_role


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Audit Log
@router.post("/", response_model=AuditLogResponse)
def create_audit_log(
    log_data: AuditLogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    audit_log = AuditLog(
        action=log_data.action,
        description=log_data.description,
        user_id=current_user.id
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log


# Get All Audit Logs
@router.get("/", response_model=list[AuditLogResponse])
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_any_role(
            "Admin",
            "Approval",
            "Reviewer",
            "Role Management"
        )
    )
):
    return db.query(AuditLog).order_by(
        AuditLog.created_at.desc()
    ).all()


# Get My Audit Logs
@router.get("/my-logs", response_model=list[AuditLogResponse])
def get_my_audit_logs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(AuditLog).filter(
        AuditLog.user_id == current_user.id
    ).order_by(
        AuditLog.created_at.desc()
    ).all()


# Get Single Audit Log
@router.get("/{log_id}", response_model=AuditLogResponse)
def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_any_role(
            "Admin",
            "Approval",
            "Reviewer",
            "Role Management"
        )
    )
):
    return db.query(AuditLog).filter(
        AuditLog.id == log_id
    ).first()