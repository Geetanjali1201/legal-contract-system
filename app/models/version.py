from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base


class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True)
    version_number = Column(Integer, nullable=False)
    file_path = Column(String(500), nullable=True)
    changes = Column(Text, nullable=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)