from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from python_test.database import get_async_db
from python_test.models.models import User
from python_test.models.schemas import RegisterUserRequest, UserModel


class UserService:
    def __init__(self, db: AsyncSession = Depends(get_async_db)) -> None:
        self.db = db

    async def users_list(self, min_age: Optional[int] = None, max_age: Optional[int] = None):
        query = select(User)
        if min_age:
            query = query.filter(User.age >= min_age)
        if max_age:
            query = query.filter(User.age <= max_age)
        result = await self.db.execute(query)
        users = result.scalars()

        return users

    async def register_user(self, user: RegisterUserRequest):

        user_object = User(**user.model_dump())
        self.db.add(user_object)
        await self.db.commit()

        return UserModel.model_validate(user_object)