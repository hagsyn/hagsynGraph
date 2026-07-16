from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.db import Base, SessionLocal, engine
from .routers import admin_router, auth_router, dashboard_router, health_router, knowledge_router, tools_router
from .services.auth import bootstrap_auth_state

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    bootstrap_auth_state(db)

app = FastAPI(title="Hagsyn Graph API", version="0.1.0")

allowed_origins = [origin.strip() for origin in settings.frontend_origin.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(tools_router)
app.include_router(dashboard_router)
app.include_router(knowledge_router)
