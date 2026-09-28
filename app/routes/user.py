from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    LoginRequest
)

from app.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.auth import (
    get_current_user,
    require_role,
    require_any_role
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
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
# LOGIN
# ==========================================

@router.post("/login")
def login_user(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == login_data.username
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        login_data.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not user.is_active:

        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    access_token = create_access_token({

        "sub": str(user.id),

        "username": user.username,

        "role_id": user.role_id

    })

    return {

        "message": "Login successful",

        "access_token": access_token,

        "token_type": "bearer"

    }


# ==========================================
# MY PROFILE
# ==========================================

@router.get("/me")
def get_my_profile(
    current_user: User = Depends(
        get_current_user
    )
):

    return {

        "id": current_user.id,

        "username": current_user.username,

        "full_name": current_user.full_name,

        "role_id": current_user.role_id,

        "is_active": current_user.is_active

    }


# ==========================================
# ADMIN ONLY
# ==========================================

@router.get("/admin-only")
def admin_only(
    current_user: User = Depends(
        require_role("Admin")
    )
):

    return {

        "message": "Welcome Admin",

        "username": current_user.username,

        "role": "Admin"

    }


# ==========================================
# LOGOUT
# ==========================================

@router.post("/logout")
def logout_user(
    current_user: User = Depends(
        get_current_user
    )
):

    return {

        "message": "Logout successful",

        "username": current_user.username

    }


# ==========================================
# REVIEWER ONLY
# ==========================================

@router.get("/reviewer-only")
def reviewer_only(
    current_user: User = Depends(
        require_role("Reviewer")
    )
):

    return {

        "message": "Welcome Reviewer",

        "username": current_user.username,

        "role": "Reviewer"

    }


# ==========================================
# APPROVAL ONLY
# ==========================================

@router.get("/approval-only")
def approval_only(
    current_user: User = Depends(
        require_role("Approval")
    )
):

    return {

        "message": "Welcome Approval User",

        "username": current_user.username,

        "role": "Approval"

    }


# ==========================================
# ROLE MANAGEMENT ONLY
# ==========================================

@router.get("/role-management-only")
def role_management_only(
    current_user: User = Depends(
        require_role("Role Management")
    )
):

    return {

        "message": "Welcome Role Management User",

        "username": current_user.username,

        "role": "Role Management"

    }


# ==========================================
# CREATE USER
# ADMIN + ROLE MANAGEMENT ONLY
# ==========================================

@router.post(
    "/",
    response_model=UserResponse
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Role Management")
    )
):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    role = db.query(Role).filter(
        Role.id == user.role_id
    ).first()

    if not role:

        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(

        username=user.username,

        password_hash=hashed_password,

        full_name=user.full_name,

        role_id=user.role_id,

        is_active=True

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# ==========================================
# GET ALL USERS
# ADMIN + ROLE MANAGEMENT ONLY
# ==========================================

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Role Management")
    )
):

    users = db.query(User).all()

    return users


# ==========================================
# GET SINGLE USER
# ADMIN + ROLE MANAGEMENT ONLY
# ==========================================

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Role Management")
    )
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ==========================================
# UPDATE USER
# ADMIN + ROLE MANAGEMENT ONLY
# ==========================================

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Role Management")
    )
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    role = db.query(Role).filter(
        Role.id == user_data.role_id
    ).first()

    if not role:

        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    user.full_name = user_data.full_name

    user.role_id = user_data.role_id

    user.is_active = user_data.is_active

    db.commit()

    db.refresh(user)

    return user


# ==========================================
# DELETE USER
# ADMIN + ROLE MANAGEMENT ONLY
# ==========================================

@router.delete(
    "/{user_id}"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_any_role("Admin", "Role Management")
    )
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)

    db.commit()

    return {

        "message": "User deleted successfully"

    }
















































# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database import SessionLocal
# from app.models.user import User
# from app.models.role import Role

# from app.schemas.user import (
#     UserCreate,
#     UserUpdate,
#     UserResponse,
#     LoginRequest
# )

# from app.security import (
#     hash_password,
#     verify_password,
#     create_access_token
# )

# from app.auth import (
#     get_current_user,
#     require_role,
#     require_any_role
# )


# router = APIRouter(
#     prefix="/users",
#     tags=["Users"]
# )


# # ==========================================
# # DATABASE
# # ==========================================

# def get_db():

#     db = SessionLocal()

#     try:
#         yield db

#     finally:
#         db.close()


# # ==========================================
# # CREATE USER
# # ADMIN + ROLE MANAGEMENT ONLY
# # ==========================================

# @router.post(
#     "/",
#     response_model=UserResponse
# )
# def create_user(
#     user: UserCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_any_role("Admin", "Role Management")
#     )
# ):

#     # Check username

#     existing_user = db.query(User).filter(
#         User.username == user.username
#     ).first()

#     if existing_user:

#         raise HTTPException(
#             status_code=400,
#             detail="Username already exists"
#         )


#     # Check role

#     role = db.query(Role).filter(
#         Role.id == user.role_id
#     ).first()

#     if not role:

#         raise HTTPException(
#             status_code=404,
#             detail="Role not found"
#         )


#     # Hash password

#     hashed_password = hash_password(
#         user.password
#     )


#     # Create user

#     new_user = User(

#         username=user.username,

#         password_hash=hashed_password,

#         full_name=user.full_name,

#         role_id=user.role_id,

#         is_active=True

#     )


#     db.add(new_user)

#     db.commit()

#     db.refresh(new_user)


#     return new_user


# # ==========================================
# # GET ALL USERS
# # ADMIN + ROLE MANAGEMENT ONLY
# # ==========================================

# @router.get(
#     "/",
#     response_model=list[UserResponse]
# )
# def get_users(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_any_role("Admin", "Role Management")
#     )
# ):

#     users = db.query(User).all()

#     return users


# # ==========================================
# # GET SINGLE USER
# # ADMIN + ROLE MANAGEMENT ONLY
# # ==========================================

# @router.get(
#     "/{user_id}",
#     response_model=UserResponse
# )
# def get_user(
#     user_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_any_role("Admin", "Role Management")
#     )
# ):

#     user = db.query(User).filter(
#         User.id == user_id
#     ).first()


#     if not user:

#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )


#     return user


# # ==========================================
# # UPDATE USER
# # ADMIN + ROLE MANAGEMENT ONLY
# # ==========================================

# @router.put(
#     "/{user_id}",
#     response_model=UserResponse
# )
# def update_user(
#     user_id: int,
#     user_data: UserUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_any_role("Admin", "Role Management")
#     )
# ):

#     user = db.query(User).filter(
#         User.id == user_id
#     ).first()


#     if not user:

#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )


#     # Check role

#     role = db.query(Role).filter(
#         Role.id == user_data.role_id
#     ).first()


#     if not role:

#         raise HTTPException(
#             status_code=404,
#             detail="Role not found"
#         )


#     # Update user

#     user.full_name = user_data.full_name

#     user.role_id = user_data.role_id

#     user.is_active = user_data.is_active


#     db.commit()

#     db.refresh(user)


#     return user


# # ==========================================
# # DELETE USER
# # ADMIN + ROLE MANAGEMENT ONLY
# # ==========================================

# @router.delete(
#     "/{user_id}"
# )
# def delete_user(
#     user_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(
#         require_any_role("Admin", "Role Management")
#     )
# ):

#     user = db.query(User).filter(
#         User.id == user_id
#     ).first()


#     if not user:

#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )


#     db.delete(user)

#     db.commit()


#     return {
#         "message": "User deleted successfully"
#     }


# # ==========================================
# # LOGIN
# # ==========================================

# @router.post("/login")
# def login_user(
#     login_data: LoginRequest,
#     db: Session = Depends(get_db)
# ):

#     user = db.query(User).filter(
#         User.username == login_data.username
#     ).first()


#     if not user:

#         raise HTTPException(
#             status_code=401,
#             detail="Invalid username or password"
#         )


#     if not verify_password(
#         login_data.password,
#         user.password_hash
#     ):

#         raise HTTPException(
#             status_code=401,
#             detail="Invalid username or password"
#         )


#     if not user.is_active:

#         raise HTTPException(
#             status_code=403,
#             detail="User account is inactive"
#         )


#     access_token = create_access_token({

#         "sub": str(user.id),

#         "username": user.username,

#         "role_id": user.role_id

#     })


#     return {

#         "message": "Login successful",

#         "access_token": access_token,

#         "token_type": "bearer"

#     }


# # ==========================================
# # MY PROFILE
# # ==========================================

# @router.get("/me")
# def get_my_profile(
#     current_user: User = Depends(
#         get_current_user
#     )
# ):

#     return {

#         "id": current_user.id,

#         "username": current_user.username,

#         "full_name": current_user.full_name,

#         "role_id": current_user.role_id,

#         "is_active": current_user.is_active

#     }


# # ==========================================
# # ADMIN ONLY
# # ==========================================

# @router.get("/admin-only")
# def admin_only(
#     current_user: User = Depends(
#         require_role("Admin")
#     )
# ):

#     return {

#         "message": "Welcome Admin",

#         "username": current_user.username,

#         "role": "Admin"

#     }


# # ==========================================
# # LOGOUT
# # ==========================================

# @router.post("/logout")
# def logout_user(
#     current_user: User = Depends(
#         get_current_user
#     )
# ):

#     return {

#         "message": "Logout successful",

#         "username": current_user.username

#     }


# # ==========================================
# # REVIEWER ONLY
# # ==========================================

# @router.get("/reviewer-only")
# def reviewer_only(
#     current_user: User = Depends(
#         require_role("Reviewer")
#     )
# ):

#     return {

#         "message": "Welcome Reviewer",

#         "username": current_user.username,

#         "role": "Reviewer"

#     }


# # ==========================================
# # APPROVAL ONLY
# # ==========================================

# @router.get("/approval-only")
# def approval_only(
#     current_user: User = Depends(
#         require_role("Approval")
#     )
# ):

#     return {

#         "message": "Welcome Approval User",

#         "username": current_user.username,

#         "role": "Approval"

#     }


# # ==========================================
# # ROLE MANAGEMENT ONLY
# # ==========================================

# @router.get("/role-management-only")
# def role_management_only(
#     current_user: User = Depends(
#         require_role("Role Management")
#     )
# ):

#     return {

#         "message": "Welcome Role Management User",

#         "username": current_user.username,

#         "role": "Role Management"

#     }






































# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database import SessionLocal
# from app.models.user import User
# from app.models.role import Role
# # from app.schemas.user import UserCreate, UserResponse
# # from app.security import hash_password
# from app.schemas.user import UserCreate, UserResponse, LoginRequest
# from app.security import hash_password, verify_password, create_access_token
# from app.auth import get_current_user
# from app.auth import get_current_user, require_role



# router = APIRouter(
#     prefix="/users",
#     tags=["Users"]
# )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.post("/", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):

#     # Check username already exists
#     existing_user = db.query(User).filter(
#         User.username == user.username
#     ).first()

#     if existing_user:
#         raise HTTPException(
#             status_code=400,
#             detail="Username already exists"
#         )

#     # Check role exists
#     role = db.query(Role).filter(
#         Role.id == user.role_id
#     ).first()

#     if not role:
#         raise HTTPException(
#             status_code=404,
#             detail="Role not found"
#         )

#     # Hash password
#     hashed_password = hash_password(user.password)

#     # Create user
#     new_user = User(
#         username=user.username,
#         password_hash=hashed_password,
#         full_name=user.full_name,
#         role_id=user.role_id
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user

# @router.post("/login")
# def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):

#     user = db.query(User).filter(
#         User.username == login_data.username
#     ).first()

#     if not user:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid username or password"
#         )

#     if not verify_password(
#         login_data.password,
#         user.password_hash
#     ):
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid username or password"
#         )

#     if not user.is_active:
#         raise HTTPException(
#             status_code=403,
#             detail="User account is inactive"
#         )

#     access_token = create_access_token(
#         {
#             "sub": str(user.id),
#             "username": user.username,
#             "role_id": user.role_id
#         }
#     )

#     return {
#         "message": "Login successful",
#         "access_token": access_token,
#         "token_type": "bearer"
#     }

# @router.get("/me")
# def get_my_profile(
#     current_user: User = Depends(get_current_user)
# ):
#     return {
#         "id": current_user.id,
#         "username": current_user.username,
#         "full_name": current_user.full_name,
#         "role_id": current_user.role_id,
#         "is_active": current_user.is_active
#     }

# @router.get("/admin-only")
# def admin_only(
#     current_user: User = Depends(require_role("Admin"))
# ):
#     return {
#         "message": "Welcome Admin",
#         "username": current_user.username,
#         "role": "Admin"
#     }

# #Logout API
# @router.post("/logout")
# def logout_user(
#     current_user: User = Depends(get_current_user)
# ):
#     return {
#         "message": "Logout successful",
#         "username": current_user.username
#     }

# @router.get("/reviewer-only")
# def reviewer_only(
#     current_user: User = Depends(require_role("Reviewer"))
# ):
#     return {
#         "message": "Welcome Reviewer",
#         "username": current_user.username,
#         "role": "Reviewer"
#     }

# @router.get("/approval-only")
# def approval_only(
#     current_user: User = Depends(require_role("Approval"))
# ):
#     return {
#         "message": "Welcome Approval User",
#         "username": current_user.username,
#         "role": "Approval"
#     }

# @router.get("/role-management-only")
# def role_management_only(
#     current_user: User = Depends(require_role("Role Management"))
# ):
#     return {
#         "message": "Welcome Role Management User",
#         "username": current_user.username,
#         "role": "Role Management"
#     }