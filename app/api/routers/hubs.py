from typing import Annotated, List
from fastapi import APIRouter, Query, HTTPException
from app.api.deps import SessionDep
from app.models.hubs import Hub, HubCreate, HubPublic
from sqlmodel import select

router = APIRouter(prefix="/hubs", tags=["hubs"])


@router.post("/", response_model=HubPublic)
def create_hub(hub: HubCreate, session: SessionDep):
    db_hub = Hub.model_validate(hub)
    session.add(db_hub)
    session.commit()
    session.refresh(db_hub)
    return db_hub


@router.get("/", response_model=List[HubPublic])
def read_hubs(session: SessionDep,
              offset: int = 0,
              limit: Annotated[int, Query(le=100)] = 25
              ):
    hubs = session.exec(select(Hub).offset(offset).limit(limit)).all()
    return hubs


@router.get("/{hub_id}", response_model=HubPublic)
def read_hub(hub_id: int, session: SessionDep):
    hub = session.get(Hub, hub_id)
    if not hub:
        raise HTTPException(status_code=404, detail="Hub not found")
    return hub
