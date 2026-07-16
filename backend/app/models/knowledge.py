from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db import Base


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:16]}"


class Node(Base):
    __tablename__ = "nodes"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("node"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    url: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="todo", nullable=False)
    importance: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    business_value: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tags: Mapped[List["NodeTag"]] = relationship(back_populates="node", cascade="all, delete-orphan")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("tag"))
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    nodes: Mapped[List["NodeTag"]] = relationship(back_populates="tag", cascade="all, delete-orphan")


class NodeTag(Base):
    __tablename__ = "node_tags"
    __table_args__ = (UniqueConstraint("node_id", "tag_id", name="uq_node_tag"),)

    node_id: Mapped[str] = mapped_column(ForeignKey("nodes.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[str] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    node: Mapped[Node] = relationship(back_populates="tags")
    tag: Mapped[Tag] = relationship(back_populates="nodes")


class Edge(Base):
    __tablename__ = "edges"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("edge"))
    source_id: Mapped[str] = mapped_column(ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False)
    target_id: Mapped[str] = mapped_column(ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False)
    relation: Mapped[str] = mapped_column(String(80), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("roadmap"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    target_user: Mapped[Optional[str]] = mapped_column(String(255))
    goal: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    steps: Mapped[List["RoadmapStep"]] = relationship(
        back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapStep.step_order"
    )


class RoadmapStep(Base):
    __tablename__ = "roadmap_steps"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("step"))
    roadmap_id: Mapped[str] = mapped_column(ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False)
    node_id: Mapped[Optional[str]] = mapped_column(ForeignKey("nodes.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="todo", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    roadmap: Mapped[Roadmap] = relationship(back_populates="steps")
