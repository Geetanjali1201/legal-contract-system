from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(20), default="Pending", nullable=False)
    comments = Column(Text, nullable=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)