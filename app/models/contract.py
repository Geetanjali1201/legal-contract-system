from sqlalchemy import Column, Integer, String, Text, Date
from app.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="Draft", nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)