from fastapi import APIRouter
from ..deps import SessionDep

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def users(db = SessionDep):
    return {"username": "fakecurrentuser"}