# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from app.database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(100), unique=True, nullable=False)
#     email = Column(String(150), unique=True, nullable=False)
#     password = Column(String(255), nullable=False)
#     is_active = Column(Boolean, default=True)
#     role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False, index=True)

    password_hash = Column(String(255), nullable=False)

    full_name = Column(String(150), nullable=False)

    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("Role")