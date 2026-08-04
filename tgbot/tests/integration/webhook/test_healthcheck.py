from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from infra.webhook.router import webhook_router


def test_healthcheck_returns_ok() -> None:
    app = FastAPI()
    app.include_router(webhook_router)

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
