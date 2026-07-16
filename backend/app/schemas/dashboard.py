from pydantic import BaseModel

from .knowledge import NodeOut


class DashboardOut(BaseModel):
    totalNodes: int
    tools: int
    projects: int
    resources: int
    roadmaps: int
    recentNodes: list[NodeOut]
