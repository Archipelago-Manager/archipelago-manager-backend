from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.hubs import Hub


def test_upload_file_hub(client: TestClient, hub: Hub, session: Session):
    with open('test_files/test.yaml', 'rb') as f:
        file_j = {'file': f}
        response = client.post(
                f"/hubs/{hub.id}/upload_file/testing/test.yaml?desc=test",
                files=file_j)
        data = response.json()

    assert response.status_code == 200
    assert data["path"] == f"hubs/{hub.id}/testing/test.yaml"
    assert data["description"] == "test"
