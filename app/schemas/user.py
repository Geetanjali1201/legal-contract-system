from pydantic import BaseModel


# ==========================================
# CREATE USER
# ==========================================

class UserCreate(BaseModel):

    username: str

    password: str

    full_name: str

    role_id: int


# ==========================================
# UPDATE USER
# ==========================================

class UserUpdate(BaseModel):

    full_name: str

    role_id: int

    is_active: bool


# ==========================================
# USER RESPONSE
# ==========================================

class UserResponse(BaseModel):

    id: int

    username: str

    full_name: str

    is_active: bool

    role_id: int

    class Config:
        from_attributes = True


# ==========================================
# LOGIN
# ==========================================

class LoginRequest(BaseModel):

    username: str

    password: str


















# from pydantic import BaseModel


# class UserCreate(BaseModel):
#     username: str
#     password: str
#     full_name: str
#     role_id: int


# class UserResponse(BaseModel):
#     id: int
#     username: str
#     full_name: str
#     is_active: bool
#     role_id: int

#     class Config:
#         from_attributes = True


# class LoginRequest(BaseModel):
#     username: str
#     password: str