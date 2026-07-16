from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.auth import require_auth
from ..core.db import get_db
from ..schemas.dashboard import DashboardOut
from ..services.dashboard import build_dashboard

router = APIRouter()


@router.get("/api/dashboard", response_model=DashboardOut)
def dashboard(_: str = Depends(require_auth), db: Session = Depends(get_db)):
    return build_dashboard(db)
