from pathlib import Path
from typing import Annotated, List
from fastapi import APIRouter, Query, HTTPException, UploadFile, Depends
from fastapi.responses import Response
from sqlmodel import select
from app.api.deps import SessionDep
from app.models.hubs import Hub, HubCreate, HubPublic, HubPrivate
from app.models.files import (
        File,
        FileCreateHub,
        FilePublic,
        FileType,
        FiletypeToEnum
        )
from app.core.file_manager import file_manager
from app.api.utils import get_and_verify_hub


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


@router.post("/{hub_id}/upload_file/{file_path:path}",
             response_model=FilePublic)
def upload_file(file_path: str,
                file: UploadFile, session: SessionDep,
                hub: Annotated[Hub, Depends(get_and_verify_hub)],
                desc: str | None = None,
                ):
    new_path = Path(f"hubs/{hub.id}/") / file_path
    # TODO: Check that file path and file suffix is the same
    ft = FiletypeToEnum(new_path.suffix)
    if ft not in [FileType.APWORLD, FileType.YAML]:
        raise HTTPException(status_code=400,
                            detail=f"Filetype {ft} not allowed")
    try:
        file_manager.write(file.file, new_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error raised: {e}")
    db_file = File.model_validate(FileCreateHub(path=str(new_path),
                                                description=desc,
                                                owner_hub_id=hub.id,
                                                file_type=ft
                                                ))
    session.add(db_file)
    session.add(hub)
    session.commit()
    session.refresh(db_file)
    return db_file


@router.get("/download_file/{file_path:path}")
def download_file(file_path: str):
    ret_file = file_manager.read(file_path)

    return Response(content=ret_file.read(),
                    media_type='application/octet-stream')
