from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.routes import version
from app.routes import audit_log

from app.database import Base, engine, SessionLocal

import app.models

from app.models.contract import Contract
from app.models.document import Document

from app.routes.role import router as role_router
from app.routes.user import router as user_router
from app.routes.contract import router as contract_router
from app.routes.document import router as document_router
from app.routes.approval import router as approval_router
from app.routes.clause import router as clause_router
from app.routes.modification import router as modification_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Legal Contract Document Modification System"
)


# =========================
# Static Files
# =========================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# =========================
# HTML Templates
# =========================

templates = Jinja2Templates(
    directory="templates"
)


# =========================
# API Routers
# =========================

app.include_router(role_router)
app.include_router(user_router)
app.include_router(contract_router)
app.include_router(document_router)
app.include_router(approval_router)
app.include_router(clause_router)
app.include_router(modification_router)
app.include_router(version.router)
app.include_router(audit_log.router)

# =========================
# Database Session
# =========================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================
# Home API
# =========================

@app.get("/")
def home():
    return {
        "message": "Legal Contract System API is running"
    }


# =========================
# Login Page
# =========================

@app.get("/login")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


# =========================
# Dashboard Page
# =========================

@app.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    # Total contracts
    total_contracts = db.query(Contract).count()

    # Draft contracts
    draft_contracts = db.query(Contract).filter(
        Contract.status == "Draft"
    ).count()

    # Active contracts
    active_contracts = db.query(Contract).filter(
        Contract.status == "Active"
    ).count()

    # Total documents
    total_documents = db.query(Document).count()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_contracts": total_contracts,
            "draft_contracts": draft_contracts,
            "active_contracts": active_contracts,
            "total_documents": total_documents
        }
    )


# =========================
# Contracts Page
# =========================

@app.get("/contracts-page")
def contracts_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="contracts.html",
        context={}
    )


# =========================
# Documents Page
# =========================

@app.get("/documents-page")
def documents_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="documents.html",
        context={}
    )


# =========================
# Users Page
# =========================

@app.get("/users-page")
def users_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={}
    )


# =========================
# Roles Page
# =========================

@app.get("/roles-page")
def roles_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="roles.html",
        context={}
    )


# =========================
# Approval Page
# =========================

@app.get("/approval-page")
def approval_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="approval.html",
        context={}
    )

@app.get("/modifications-page")
def modifications_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="modifications.html",
        context={}
    )

@app.get("/version-history-page")
def version_history_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="version_history.html",
        context={}
    )

@app.get("/audit-logs-page")
def audit_logs_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="audit_logs.html",
        context={}
    )









































# from fastapi import FastAPI, Request
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

# from app.database import Base, engine

# import app.models

# from app.routes.role import router as role_router
# from app.routes.user import router as user_router
# from app.routes.contract import router as contract_router
# from app.routes.document import router as document_router


# Base.metadata.create_all(bind=engine)


# app = FastAPI(
#     title="Legal Contract Document Modification System"
# )


# # Static files
# app.mount(
#     "/static",
#     StaticFiles(directory="static"),
#     name="static"
# )


# # HTML Templates
# templates = Jinja2Templates(
#     directory="templates"
# )


# # API Routers
# app.include_router(role_router)
# app.include_router(user_router)
# app.include_router(contract_router)
# app.include_router(document_router)


# # Home API
# @app.get("/")
# def home():
#     return {
#         "message": "Legal Contract System API is running"
#     }


# @app.get("/dashboard")
# def dashboard(request: Request):

#     return templates.TemplateResponse(
#         request=request,
#         name="dashboard.html",
#         context={}
#     )


























# from fastapi import FastAPI

# from app.database import Base, engine

# import app.models

# from app.routes.role import router as role_router
# from app.routes.user import router as user_router
# from app.routes.contract import router as contract_router
# from app.routes.document import router as document_router

# Base.metadata.create_all(bind=engine)


# app = FastAPI(
#     title="Legal Contract Document Modification System"
# )


# app.include_router(role_router)
# app.include_router(user_router)
# app.include_router(contract_router)
# app.include_router(document_router)


# @app.get("/")
# def home():

#     return {
#         "message": "Legal Contract System API is running"
#     }