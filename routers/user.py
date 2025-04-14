from fastapi import APIRouter
from database import db_dependency
from schemas.user import UserCreate
from models.user import UserModel
from starlette import status

router = APIRouter(
    prefix="/users",
    tags=['user'],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: db_dependency):
    print(user)
    db_user = UserModel(email=user.email)
    db.add(db_user)
    await db.flush()
    await db.refresh(db_user)

    return db_user


