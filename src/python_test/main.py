from fastapi import FastAPI, APIRouter

from .routers.city import city_router
from .routers.picnic import picnic_router
from .routers.user import user_router

app = FastAPI(title='Test task from Unlim Soft')

main_api_router = APIRouter()

main_api_router.include_router(city_router, prefix='/city', tags=['city'])
main_api_router.include_router(user_router, prefix='/user', tags=['user'])
main_api_router.include_router(picnic_router, prefix='/picnic', tags=['picnic'])

app.include_router(main_api_router)
