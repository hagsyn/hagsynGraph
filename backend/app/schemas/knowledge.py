from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from typing import Literal

from pydantic import BaseModel, Field

NodeType = Literal["tool", "model", "framework", "use_case", "project", "resource", "skill", "roadmap"]
NodeStatus = Literal["todo", "learning", "used", "mastered"]
StepStatus = Literal["todo", "learning", "done"]


class NodeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    type: NodeType
    description: Optional[str] = None
    tags: List[str] = []
    url: Optional[str] = None
    status: NodeStatus = "todo"
    importance: int = Field(default=3, ge=1, le=5)
    businessValue: int = Field(default=3, ge=1, le=5)
    note: Optional[str] = None


class NodeUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    type: Optional[NodeType] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    url: Optional[str] = None
    status: Optional[NodeStatus] = None
    importance: Optional[int] = Field(default=None, ge=1, le=5)
    businessValue: Optional[int] = Field(default=None, ge=1, le=5)
    note: Optional[str] = None


class NodeOut(BaseModel):
    id: str
    title: str
    type: str
    description: Optional[str]
    tags: List[str]
    url: Optional[str]
    status: str
    importance: int
    businessValue: int
    note: Optional[str]
    createdAt: datetime
    updatedAt: datetime


class EdgeCreate(BaseModel):
    sourceId: str
    targetId: str
    relation: str = Field(min_length=1, max_length=80)
    note: Optional[str] = None


class EdgeOut(BaseModel):
    id: str
    sourceId: str
    targetId: str
    relation: str
    note: Optional[str]
    createdAt: datetime
    updatedAt: datetime


class RoadmapCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    targetUser: Optional[str] = None
    goal: Optional[str] = None


class RoadmapStepCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    nodeId: Optional[str] = None
    status: StepStatus = "todo"


class RoadmapStepOut(BaseModel):
    id: str
    roadmapId: str
    nodeId: Optional[str]
    title: str
    description: Optional[str]
    order: int
    status: str


class RoadmapOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    targetUser: Optional[str]
    goal: Optional[str]
    steps: List[RoadmapStepOut] = []
    createdAt: datetime
    updatedAt: datetime
