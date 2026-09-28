from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)