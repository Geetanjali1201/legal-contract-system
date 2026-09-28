from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.version import Version
from app.models.contract import Contract
from app.schemas.version import VersionCreate, VersionResponse

from app.auth import get_current_user, require_any_role


router = APIRouter(prefix="/versions", tags=["Versions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Version
@router.post("/", response_model=VersionResponse)
def create_version(
    version_data: VersionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_any_role("Admin", "Approval")
    )
):
    contract = db.query(Contract).filter(
        Contract.id == version_data.contract_id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    version = Version(
        version_number=version_data.version_number,
        file_path=version_data.file_path,
        changes=version_data.changes,
        contract_id=version_data.contract_id,
        created_by=current_user.id
    )

    db.add(version)
    db.commit()
    db.refresh(version)

    return version


# Get All Versions
@router.get("/", response_model=list[VersionResponse])
def get_versions(
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
    return db.query(Version).order_by(
        Version.contract_id,
        Version.version_number
    ).all()


# Get Version History of a Contract
@router.get(
    "/contract/{contract_id}",
    response_model=list[VersionResponse]
)
def get_contract_versions(
    contract_id: int,
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
    contract = db.query(Contract).filter(
        Contract.id == contract_id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    return db.query(Version).filter(
        Version.contract_id == contract_id
    ).order_by(
        Version.version_number
    ).all()


# Get Single Version
@router.get(
    "/{version_id}",
    response_model=VersionResponse
)
def get_version(
    version_id: int,
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
    version = db.query(Version).filter(
        Version.id == version_id
    ).first()

    if not version:
        raise HTTPException(
            status_code=404,
            detail="Version not found"
        )

    return version