from sqlalchemy import Column, Integer, Text, ForeignKey
from app.database import Base


class Clause(Base):
    __tablename__ = "clauses"

    id = Column(Integer, primary_key=True, index=True)
    clause_text = Column(Text, nullable=False)
    contract_id = Column(
        Integer,
        ForeignKey("contracts.id"),
        nullable=False
    )



















# from sqlalchemy import Column, Integer, Text, ForeignKey
# from app.database import Base


# class Clause(Base):
#     __tablename__ = "clauses"

#     id = Column(Integer, primary_key=True, index=True)
#     clause_text = Column(Text, nullable=False)
#     contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)