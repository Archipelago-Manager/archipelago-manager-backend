from sqlmodel import Session
from app.tests.utils.utils import random_lower_string
from app.models.hubs import Hub, HubCreate


def create_random_hub(session: Session, description=True) -> Hub:
    name = random_lower_string()
    if description:
        description = random_lower_string()
        hub = Hub.model_validate(HubCreate(name=name, description=description))
    else:
        hub = Hub.model_validate(HubCreate(name=name))
    session.add(hub)
    session.commit()
    session.refresh(hub)
    return hub
