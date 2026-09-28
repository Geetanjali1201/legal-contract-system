from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleResponse

from app.auth import require_any_role
from app.models.user import User


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


# ==========================================
# DATABASE
# ==========================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ==========================================
# CREATE ROLE
# ADMIN + ROLE MANAGEMENT ONLY
# ==========================================

@router.post(
    "/",
    response_model=RoleResponse
)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Role Management")
    )
):

    existing_role = db.query(Role).filter(
        Role.name == role.name
    ).first()

    if existing_role:
        raise HTTPException(
            status_code=400,
            detail="Role already exists"
        )

    new_role = Role(
        name=role.name
    )

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


# ==========================================
# GET ALL ROLES
# ADMIN + ROLE MANAGEMENT ONLY
# ==========================================

@router.get(
    "/",
    response_model=list[RoleResponse]
)
def get_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Role Management")
    )
):

    roles = db.query(Role).all()

    return roles


# ==========================================
# GET ROLE BY ID
# ADMIN + ROLE MANAGEMENT ONLY
# ==========================================

@router.get(
    "/{role_id}",
    response_model=RoleResponse
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Role Management")
    )
):

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    return role


# ==========================================
# UPDATE ROLE
# ADMIN + ROLE MANAGEMENT ONLY
# ==========================================

@router.put(
    "/{role_id}",
    response_model=RoleResponse
)
def update_role(
    role_id: int,
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Role Management")
    )
):

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    role.name = role_data.name

    db.commit()
    db.refresh(role)

    return role


# ==========================================
# DELETE ROLE
# ADMIN + ROLE MANAGEMENT ONLY
# ==========================================

@router.delete(
    "/{role_id}"
)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Role Management")
    )
):

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    db.delete(role)
    db.commit()

    return {
        "message": "Role deleted successfully"
    }






























# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database import SessionLocal
# from app.models.role import Role
# from app.schemas.role import RoleCreate, RoleResponse


# router = APIRouter(
#     prefix="/roles",
#     tags=["Roles"]
# )


# def get_db():
#     db = SessionLocal()

#     try:
#         yield db
#     finally:
#         db.close()


# # CREATE ROLE
# @router.post("/", response_model=RoleResponse)
# def create_role(role: RoleCreate, db: Session = Depends(get_db)):

#     existing_role = db.query(Role).filter(Role.name == role.name).first()

#     if existing_role:
#         raise HTTPException(
#             status_code=400,
#             detail="Role already exists"
#         )

#     new_role = Role(name=role.name)

#     db.add(new_role)
#     db.commit()
#     db.refresh(new_role)

#     return new_role


# # GET ALL ROLES
# @router.get("/", response_model=list[RoleResponse])
# def get_roles(db: Session = Depends(get_db)):

#     roles = db.query(Role).all()

#     return roles


# # GET ROLE BY ID
# @router.get("/{role_id}", response_model=RoleResponse)
# def get_role(role_id: int, db: Session = Depends(get_db)):

#     role = db.query(Role).filter(Role.id == role_id).first()

#     if not role:
#         raise HTTPException(
#             status_code=404,
#             detail="Role not found"
#         )

#     return role


# # UPDATE ROLE
# @router.put("/{role_id}", response_model=RoleResponse)
# def update_role(
#     role_id: int,
#     role_data: RoleCreate,
#     db: Session = Depends(get_db)
# ):

#     role = db.query(Role).filter(Role.id == role_id).first()

#     if not role:
#         raise HTTPException(
#             status_code=404,
#             detail="Role not found"
#         )

#     role.name = role_data.name

#     db.commit()
#     db.refresh(role)

#     return role


# # DELETE ROLE
# @router.delete("/{role_id}")
# def delete_role(role_id: int, db: Session = Depends(get_db)):

#     role = db.query(Role).filter(Role.id == role_id).first()

#     if not role:
#         raise HTTPException(
#             status_code=404,
#             detail="Role not found"
#         )

#     db.delete(role)
#     db.commit()

#     return {
#         "message": "Role deleted successfully"
#     }