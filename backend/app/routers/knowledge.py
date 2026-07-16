from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.auth import require_auth
from ..core.db import get_db
from ..models import Edge, Node, Roadmap, RoadmapStep
from ..schemas.knowledge import EdgeCreate, EdgeOut, NodeCreate, NodeOut, NodeUpdate, RoadmapCreate, RoadmapOut, RoadmapStepCreate
from ..seed_data import seed_demo_data
from ..services.knowledge import serialize_edge, serialize_node, serialize_roadmap, sync_tags

router = APIRouter()


@router.post("/api/seed")
def seed_data(_: str = Depends(require_auth), db: Session = Depends(get_db)):
    # Seed remains an explicit authenticated action because it mutates the local
    # workspace dataset and is only meant for controlled bootstrap/test usage.
    return seed_demo_data(db)


@router.post("/api/nodes", response_model=NodeOut)
def create_node(payload: NodeCreate, _: str = Depends(require_auth), db: Session = Depends(get_db)):
    # Knowledge routes still create ORM objects directly; shared normalization
    # lives in services so this module does not duplicate tag logic.
    node = Node(
        title=payload.title,
        type=payload.type,
        description=payload.description,
        url=payload.url,
        status=payload.status,
        importance=payload.importance,
        business_value=payload.businessValue,
        note=payload.note,
    )
    db.add(node)
    db.flush()
    sync_tags(db, node, payload.tags)
    db.commit()
    db.refresh(node)
    return serialize_node(node)


@router.get("/api/nodes", response_model=list[NodeOut])
def list_nodes(
    keyword: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    tag: Optional[str] = None,
    _: str = Depends(require_auth),
    db: Session = Depends(get_db),
):
    nodes = db.scalars(select(Node).order_by(Node.updated_at.desc())).all()
    # Filtering is kept application-side for now because the MVP dataset is
    # small and we want predictable semantics across combined filters.
    if keyword:
        lowered = keyword.lower()
        nodes = [node for node in nodes if lowered in node.title.lower() or lowered in (node.description or "").lower()]
    if type:
        nodes = [node for node in nodes if node.type == type]
    if status:
        nodes = [node for node in nodes if node.status == status]
    if tag:
        nodes = [node for node in nodes if tag in [node_tag.tag.name for node_tag in node.tags]]
    return [serialize_node(node) for node in nodes]


@router.get("/api/nodes/{node_id}", response_model=NodeOut)
def get_node(node_id: str, _: str = Depends(require_auth), db: Session = Depends(get_db)):
    node = db.get(Node, node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return serialize_node(node)


@router.put("/api/nodes/{node_id}", response_model=NodeOut)
def update_node(node_id: str, payload: NodeUpdate, _: str = Depends(require_auth), db: Session = Depends(get_db)):
    node = db.get(Node, node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    data = payload.model_dump(exclude_unset=True)
    if "businessValue" in data:
        node.business_value = data.pop("businessValue")
    if "tags" in data:
        # Tags need explicit sync because the API uses a flat string list while
        # persistence goes through the association table.
        sync_tags(db, node, data.pop("tags"))
    for key, value in data.items():
        setattr(node, key, value)
    db.commit()
    db.refresh(node)
    return serialize_node(node)


@router.delete("/api/nodes/{node_id}")
def delete_node(node_id: str, _: str = Depends(require_auth), db: Session = Depends(get_db)):
    node = db.get(Node, node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    db.delete(node)
    db.commit()
    return {"ok": True}


@router.post("/api/edges", response_model=EdgeOut)
def create_edge(payload: EdgeCreate, _: str = Depends(require_auth), db: Session = Depends(get_db)):
    # Edge creation validates endpoints eagerly so the graph never stores
    # dangling relations to non-existent nodes.
    if db.get(Node, payload.sourceId) is None or db.get(Node, payload.targetId) is None:
        raise HTTPException(status_code=400, detail="Source or target node not found")
    edge = Edge(source_id=payload.sourceId, target_id=payload.targetId, relation=payload.relation, note=payload.note)
    db.add(edge)
    db.commit()
    db.refresh(edge)
    return serialize_edge(edge)


@router.get("/api/edges", response_model=list[EdgeOut])
def list_edges(_: str = Depends(require_auth), db: Session = Depends(get_db)):
    return [serialize_edge(edge) for edge in db.scalars(select(Edge).order_by(Edge.created_at.desc())).all()]


@router.delete("/api/edges/{edge_id}")
def delete_edge(edge_id: str, _: str = Depends(require_auth), db: Session = Depends(get_db)):
    edge = db.get(Edge, edge_id)
    if edge is None:
        raise HTTPException(status_code=404, detail="Edge not found")
    db.delete(edge)
    db.commit()
    return {"ok": True}


@router.post("/api/roadmaps", response_model=RoadmapOut)
def create_roadmap(payload: RoadmapCreate, _: str = Depends(require_auth), db: Session = Depends(get_db)):
    roadmap = Roadmap(title=payload.title, description=payload.description, target_user=payload.targetUser, goal=payload.goal)
    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)
    return serialize_roadmap(roadmap)


@router.get("/api/roadmaps", response_model=list[RoadmapOut])
def list_roadmaps(_: str = Depends(require_auth), db: Session = Depends(get_db)):
    return [serialize_roadmap(roadmap) for roadmap in db.scalars(select(Roadmap).order_by(Roadmap.updated_at.desc())).all()]


@router.post("/api/roadmaps/{roadmap_id}/steps", response_model=RoadmapOut)
def create_roadmap_step(roadmap_id: str, payload: RoadmapStepCreate, _: str = Depends(require_auth), db: Session = Depends(get_db)):
    roadmap = db.get(Roadmap, roadmap_id)
    if roadmap is None:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    if payload.nodeId and db.get(Node, payload.nodeId) is None:
        raise HTTPException(status_code=400, detail="Node not found")
    # Step order is append-only in the current MVP. Reordering can be added
    # later without changing the current API contract.
    step = RoadmapStep(
        roadmap_id=roadmap.id,
        node_id=payload.nodeId,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        step_order=len(roadmap.steps) + 1,
    )
    db.add(step)
    db.commit()
    db.refresh(roadmap)
    return serialize_roadmap(roadmap)
