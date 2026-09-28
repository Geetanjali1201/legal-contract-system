from sqlalchemy import Column, Integer, Text, ForeignKey, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Modification(Base):
    __tablename__ = "modifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    original_value = Column(
        Text,
        nullable=False
    )

    proposed_value = Column(
        Text,
        nullable=False
    )

    modification_reason = Column(
        Text,
        nullable=True
    )

    modified_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    request_date = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    status = Column(
        String(20),
        default="PENDING",
        nullable=False
    )

    approver_comments = Column(
        Text,
        nullable=True
    )

    rejection_reason = Column(
        Text,
        nullable=True
    )

    approved_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    decision_date = Column(
        DateTime,
        nullable=True
    )

    contract_id = Column(
        Integer,
        ForeignKey("contracts.id"),
        nullable=False
    )



























# from sqlalchemy import Column, Integer, Text, ForeignKey, String, DateTime
# from sqlalchemy.sql import func

# from app.database import Base


# class Modification(Base):
#     __tablename__ = "modifications"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True
#     )

#     original_value = Column(
#         Text,
#         nullable=False
#     )

#     proposed_value = Column(
#         Text,
#         nullable=False
#     )

#     modification_reason = Column(
#         Text,
#         nullable=True
#     )

#     contract_id = Column(
#         Integer,
#         ForeignKey("contracts.id"),
#         nullable=False
#     )

#     modified_by = Column(
#         Integer,
#         ForeignKey("users.id"),
#         nullable=False
#     )

#     request_date = Column(
#         DateTime,
#         server_default=func.now(),
#         nullable=False
#     )

#     status = Column(
#         String(20),
#         default="PENDING",
#         nullable=False
#     )

#     approver_comments = Column(
#         Text,
#         nullable=True
#     )

#     rejection_reason = Column(
#         Text,
#         nullable=True
#     )

#     approved_by = Column(
#         Integer,
#         ForeignKey("users.id"),
#         nullable=True
#     )

#     decision_date = Column(
#         DateTime,
#         nullable=True
#     )










































# from sqlalchemy import Column, Integer, Text, ForeignKey
# from app.database import Base


# class Modification(Base):
#     __tablename__ = "modifications"

#     id = Column(Integer, primary_key=True, index=True)

#     modification_text = Column(
#         Text,
#         nullable=False
#     )

#     contract_id = Column(
#         Integer,
#         ForeignKey("contracts.id"),
#         nullable=False
#     )

#     modified_by = Column(
#         Integer,
#         ForeignKey("users.id"),
#         nullable=False
#     )

























# from sqlalchemy import Column, Integer, Text, ForeignKey
# from app.database import Base


# class Modification(Base):
#     __tablename__ = "modifications"

#     id = Column(Integer, primary_key=True, index=True)
#     old_text = Column(Text, nullable=False)
#     new_text = Column(Text, nullable=False)
#     clause_id = Column(Integer, ForeignKey("clauses.id"), nullable=False)
#     modified_by = Column(Integer, ForeignKey("users.id"), nullable=False)