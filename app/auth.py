from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.security import SECRET_KEY, ALGORITHM
from app.models.role import Role


security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    return user

def require_role(required_role: str):
    def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        role = db.query(Role).filter(
            Role.id == current_user.role_id
        ).first()

        if not role:
            raise HTTPException(
                status_code=403,
                detail="User role not found"
            )

        if role.name != required_role:
            raise HTTPException(
                status_code=403,
                detail="Access denied. Required role: " + required_role
            )

        return current_user

    return role_checker


def require_any_role(*required_roles: str):
    def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        role = db.query(Role).filter(
            Role.id == current_user.role_id
        ).first()

        if not role:
            raise HTTPException(
                status_code=403,
                detail="User role not found"
            )

        if role.name not in required_roles:
            raise HTTPException(
                status_code=403,
                detail="Access denied. Required role: " + ", ".join(required_roles)
            )

        return current_user

    return role_checker