from .admin import router as admin_router
from .auth import router as auth_router
from .dashboard import router as dashboard_router
from .health import router as health_router
from .knowledge import router as knowledge_router
from .tools import router as tools_router

__all__ = [
    "admin_router",
    "auth_router",
    "dashboard_router",
    "health_router",
    "knowledge_router",
    "tools_router",
]
