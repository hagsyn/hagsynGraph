from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Edge, Node, NodeTag, Roadmap, RoadmapStep, Tag
from ..schemas.knowledge import EdgeOut, NodeOut, RoadmapOut, RoadmapStepOut


def serialize_node(node: Node) -> NodeOut:
    # Keep API shape frontend-friendly here so routers can stay thin and callers
    # do not need to know about ORM naming such as business_value.
    return NodeOut(
        id=node.id,
        title=node.title,
        type=node.type,
        description=node.description,
        tags=sorted(node_tag.tag.name for node_tag in node.tags),
        url=node.url,
        status=node.status,
        importance=node.importance,
        businessValue=node.business_value,
        note=node.note,
        createdAt=node.created_at,
        updatedAt=node.updated_at,
    )


def serialize_edge(edge: Edge) -> EdgeOut:
    return EdgeOut(
        id=edge.id,
        sourceId=edge.source_id,
        targetId=edge.target_id,
        relation=edge.relation,
        note=edge.note,
        createdAt=edge.created_at,
        updatedAt=edge.updated_at,
    )


def serialize_step(step: RoadmapStep) -> RoadmapStepOut:
    return RoadmapStepOut(
        id=step.id,
        roadmapId=step.roadmap_id,
        nodeId=step.node_id,
        title=step.title,
        description=step.description,
        order=step.step_order,
        status=step.status,
    )


def serialize_roadmap(roadmap: Roadmap) -> RoadmapOut:
    return RoadmapOut(
        id=roadmap.id,
        title=roadmap.title,
        description=roadmap.description,
        targetUser=roadmap.target_user,
        goal=roadmap.goal,
        steps=[serialize_step(step) for step in roadmap.steps],
        createdAt=roadmap.created_at,
        updatedAt=roadmap.updated_at,
    )


def sync_tags(db: Session, node: Node, tags: list[str]) -> None:
    # Tags are normalized through one helper so create/update flows share the
    # same dedupe and tag-auto-create behavior.
    node.tags.clear()
    seen = []
    for raw_name in tags:
        name = raw_name.strip()
        if not name or name in seen:
            continue
        seen.append(name)
        tag = db.scalar(select(Tag).where(Tag.name == name))
        if tag is None:
            tag = Tag(name=name)
            db.add(tag)
            db.flush()
        node.tags.append(NodeTag(tag=tag))
