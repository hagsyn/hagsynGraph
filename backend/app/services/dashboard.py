from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Node, Roadmap
from ..schemas.dashboard import DashboardOut
from .knowledge import serialize_node


def build_dashboard(db: Session) -> DashboardOut:
    nodes = db.scalars(select(Node).order_by(Node.created_at.desc())).all()
    recent = nodes[:5]
    return DashboardOut(
        totalNodes=len(nodes),
        tools=sum(1 for node in nodes if node.type == "tool"),
        projects=sum(1 for node in nodes if node.type == "project"),
        resources=sum(1 for node in nodes if node.type == "resource"),
        roadmaps=db.query(Roadmap).count(),
        recentNodes=[serialize_node(node) for node in recent],
    )
