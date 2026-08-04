from fastapi import APIRouter, status
from pydantic import BaseModel

healthcheck_router = APIRouter()


class Healthcheck(BaseModel):
    status: str


@healthcheck_router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def healthcheck() -> Healthcheck:
    return Healthcheck(status="ok")
