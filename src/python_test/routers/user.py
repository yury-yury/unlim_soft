from typing import Optional, List
from fastapi import APIRouter, Depends

from python_test.models.schemas import UserModel, RegisterUserRequest
from python_test.services.user import UserService


user_router = APIRouter()


@user_router.get('/list/',
                 summary='User List',
                 description='Retrieving a list of registered users.',
                 response_model=List[UserModel],
                 tags=['user'])
async def users_list(min_age: Optional[int] = None,
                     max_age: Optional[int] = None,
                     service: UserService = Depends()) -> List[UserModel]:
    """
    Список пользователей
    """
    return await service.users_list(min_age, max_age)


@user_router.post('/register/',
                  summary='CreateUser',
                  description='New User Registration.',
                  response_model=UserModel,
                  tags=['user'])
async def register_user(user: RegisterUserRequest, service: UserService = Depends()):
    """
    Регистрация пользователя
    """
    return await service.register_user(user)

