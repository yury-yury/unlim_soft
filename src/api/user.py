from fastapi import APIRouter

from src.database import Session, User
from src.api.schemas import UserModel, RegisterUserRequest


user_router = APIRouter()


@user_router.post('/users-list/', summary='')
def users_list():
    """
    Список пользователей
    """
    users = Session().query(User).all()
    return [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]


@user_router.post('/register-user/', summary='CreateUser', response_model=UserModel)
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)
