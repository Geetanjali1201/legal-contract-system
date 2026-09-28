from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil

from app.database import SessionLocal
from app.models.document import Document
from app.models.contract import Contract

from app.auth import require_any_role
from app.models.user import User


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# Upload Document
# Allowed Roles: Admin, Approval
# =========================================================

@router.post("/upload")
def upload_document(
    contract_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval"
        )
    )
):

    # Check whether contract exists
    contract = db.query(Contract).filter(
        Contract.id == contract_id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    # Create uploads folder
    upload_folder = "uploads"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Create file path
    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Save document information in database
    new_document = Document(
        file_name=file.filename,
        file_path=file_path,
        contract_id=contract_id
    )

    db.add(new_document)

    db.commit()

    db.refresh(new_document)

    return {
        "message": "Document uploaded successfully",
        "document_id": new_document.id,
        "file_name": new_document.file_name,
        "file_path": new_document.file_path,
        "contract_id": new_document.contract_id
    }


# =========================================================
# Get All Documents
# Allowed Roles: Admin, Approval, Reviewer, Role Management
# =========================================================

@router.get("/")
def get_documents(
    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval",
            "Reviewer",
            "Role Management"
        )
    )
):

    documents = db.query(Document).all()

    return documents


# =========================================================
# Get Documents by Contract ID
# Allowed Roles: Admin, Approval, Reviewer, Role Management
# =========================================================

@router.get("/contract/{contract_id}")
def get_documents_by_contract(
    contract_id: int,
    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval",
            "Reviewer",
            "Role Management"
        )
    )
):

    # Check whether contract exists
    contract = db.query(Contract).filter(
        Contract.id == contract_id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    documents = db.query(Document).filter(
        Document.contract_id == contract_id
    ).all()

    return documents


# =========================================================
# Get Document by ID
# Allowed Roles: Admin, Approval, Reviewer, Role Management
# =========================================================

@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_any_role(
            "Admin",
            "Approval",
            "Reviewer",
            "Role Management"
        )
    )
):

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

























# from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
# from sqlalchemy.orm import Session
# import os
# import shutil

# from app.database import SessionLocal
# from app.models.document import Document
# from app.models.contract import Contract


# router = APIRouter(
#     prefix="/documents",
#     tags=["Documents"]
# )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # Upload Document
# @router.post("/upload")
# def upload_document(
#     contract_id: int,
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     # Check whether contract exists
#     contract = db.query(Contract).filter(
#         Contract.id == contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     # Create uploads folder
#     upload_folder = "uploads"

#     if not os.path.exists(upload_folder):
#         os.makedirs(upload_folder)

#     # Create file path
#     file_path = os.path.join(
#         upload_folder,
#         file.filename
#     )

#     # Save uploaded file
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # Save document information in database
#     new_document = Document(
#         file_name=file.filename,
#         file_path=file_path,
#         contract_id=contract_id
#     )

#     db.add(new_document)
#     db.commit()
#     db.refresh(new_document)

#     return {
#         "message": "Document uploaded successfully",
#         "document_id": new_document.id,
#         "file_name": new_document.file_name,
#         "file_path": new_document.file_path,
#         "contract_id": new_document.contract_id
#     }


# # Get All Documents
# @router.get("/")
# def get_documents(
#     db: Session = Depends(get_db)
# ):
#     documents = db.query(Document).all()

#     return documents

# # Get Documents by Contract ID
# @router.get("/contract/{contract_id}")
# def get_documents_by_contract(
#     contract_id: int,
#     db: Session = Depends(get_db)
# ):
#     # Check whether contract exists
#     contract = db.query(Contract).filter(
#         Contract.id == contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     documents = db.query(Document).filter(
#         Document.contract_id == contract_id
#     ).all()

#     return documents

# # Get Document by ID
# @router.get("/{document_id}")
# def get_document(
#     document_id: int,
#     db: Session = Depends(get_db)
# ):
#     document = db.query(Document).filter(
#         Document.id == document_id
#     ).first()

#     if not document:
#         raise HTTPException(
#             status_code=404,
#             detail="Document not found"
#         )

#     return document






























# from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
# from sqlalchemy.orm import Session
# import os
# import shutil

# from app.database import SessionLocal
# from app.models.document import Document
# from app.models.contract import Contract


# router = APIRouter(
#     prefix="/documents",
#     tags=["Documents"]
# )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # Upload Document
# @router.post("/upload")
# def upload_document(
#     contract_id: int,
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     # Check whether contract exists
#     contract = db.query(Contract).filter(
#         Contract.id == contract_id
#     ).first()

#     if not contract:
#         raise HTTPException(
#             status_code=404,
#             detail="Contract not found"
#         )

#     # Create uploads folder
#     upload_folder = "uploads"

#     if not os.path.exists(upload_folder):
#         os.makedirs(upload_folder)

#     # Create file path
#     file_path = os.path.join(
#         upload_folder,
#         file.filename
#     )

#     # Save uploaded file
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # Save document information in database
#     new_document = Document(
#         file_name=file.filename,
#         file_path=file_path,
#         contract_id=contract_id
#     )

#     db.add(new_document)
#     db.commit()
#     db.refresh(new_document)

#     return {
#         "message": "Document uploaded successfully",
#         "document_id": new_document.id,
#         "file_name": new_document.file_name,
#         "file_path": new_document.file_path,
#         "contract_id": new_document.contract_id
#     }