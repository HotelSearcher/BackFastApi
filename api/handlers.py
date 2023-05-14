from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserCreate, UserShow
from db.dals import UserDAL
from db.session import get_db

user_router = APIRouter()

async def _create_new_user(body: UserCreate, db) -> UserShow:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                email=body.email,
                password=body.password
            )
            return UserShow(
                user_id=user.user_id,
                email=user.email
            )

async def _get_user_by_id(user_id, db) -> Union[UserShow, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(
                user_id=user_id
            )
            if user is not None:
                return UserShow(
                    user_id=user.user_id,
                    email=user.email
                )

@user_router.post("/", response_model=UserShow)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> UserShow:
    return await _create_new_user(body, db)


@user_router.get("/", response_model=UserShow)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)) -> UserShow:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return user
