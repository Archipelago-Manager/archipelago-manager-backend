from fastapi import HTTPException
from app.api.deps import SessionDep
from app.models.hubs import Hub


async def get_and_verify_hub(hub_id: int, session: SessionDep):
    hub = session.get(Hub, hub_id)
    if not hub:
        raise HTTPException(status_code=404, detail="Hub not found")
    return hub
