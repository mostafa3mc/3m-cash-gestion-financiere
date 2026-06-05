from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import Base, engine
from .routes import setup, saisie, dashboard

Base.metadata.create_all(bind=engine)
app = FastAPI(title="3M CASH – Gestion Financière")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(setup.router, prefix="/api")
app.include_router(saisie.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

@app.get("/")
def root():
    return {"app": "3M CASH – Gestion Financière", "status": "online"}
