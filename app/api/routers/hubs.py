from typing import Annotated, List
from fastapi import APIRouter, Query, HTTPException, UploadFile
from fastapi.responses import Response
from sqlmodel import select
from app.api.deps import SessionDep
from app.models.hubs import Hub, HubCreate, HubPublic, HubPrivate
from app.core.file_manager import file_manager


router = APIRouter(prefix="/hubs", tags=["hubs"])


@router.post("/", response_model=HubPublic)
def create_hub(hub: HubCreate, session: SessionDep):
    hub_val = session.exec(select(Hub).where(Hub.name == hub.name)).first()
    if hub_val:
        raise HTTPException(
                status_code=400,
                detail="A hub with this name already exists"
                )
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


@router.get("/{hub_id}", response_model=HubPrivate)
def read_hub(hub_id: int, session: SessionDep):
    hub = session.get(Hub, hub_id)
    if not hub:
        raise HTTPException(status_code=404, detail="Hub not found")
    return hub


@router.get("/get_from_name/{hub_name}", response_model=HubPublic)
def read_hub_from_name(hub_name: str, session: SessionDep):
    hub = session.exec(select(Hub).where(Hub.name == hub_name)).first()
    if not hub:
        raise HTTPException(status_code=404, detail="Hub not found")
    return hub


@router.post("/upload_file/{file_path:path}")
def upload_file(file_path: str, file: UploadFile):
    file_manager.write(file.file, file_path)


@router.get("/download_file/{file_path:path}")
def download_file(file_path: str):
    ret_file = file_manager.read(file_path)

    return Response(content=ret_file.read(),
                    media_type='application/octet-stream')
