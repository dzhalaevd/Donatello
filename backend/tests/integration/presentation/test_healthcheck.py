from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from presentation.rest.controllers.healthcheck import healthcheck_router


def test_healthcheck_returns_ok() -> None:
    app = FastAPI()
    app.include_router(healthcheck_router, prefix="/api/v1/healthcheck")

    with TestClient(app) as client:
        response = client.get("/api/v1/healthcheck/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
