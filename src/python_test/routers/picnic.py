import datetime as dt
from typing import List, Optional

import datetime
from fastapi import Query, APIRouter, Depends

from python_test.database import SyncSession as Session
from python_test.models.models import City, Picnic, PicnicRegistration
from python_test.models.schemas import PicnicResponse, PicnicAddResponse, PicnicRegistrationResponse
from python_test.services.picnic import PicnicService

picnic_router = APIRouter()


@picnic_router.get('/all/', summary='All Picnics', tags=['picnic'], response_model=List[PicnicResponse])
async def all_picnics(datetime: datetime.datetime = Query(default=None,
                                                          description='Время пикника (по умолчанию не задано)'),
                      past: bool = Query(default=True, description='Включая уже прошедшие пикники'),
                      service: PicnicService = Depends()):
    """
    Список всех пикников
    """
    return await service.all_picnics(datetime, past)


@picnic_router.post('/add/', summary='Picnic Add', tags=['picnic'], response_model=PicnicAddResponse)
async def picnic_add(city_id: Optional[int] = None,
                     datetime: Optional[datetime.datetime] = None,
                     service: PicnicService = Depends()):
    return service.picnic_add(city_id, datetime)


@picnic_router.post('/register/',
             summary='Picnic Registration',
             tags=['picnic'],
             response_model=PicnicRegistrationResponse)
async def register_to_picnic(picnic_id: Optional[int] = Query(default=None, description='ID пикника'),
                       user_id: Optional[int] = Query(default=None, description='ID участника'),
                       service: PicnicService = Depends()):
    """
    Регистрация пользователя на пикник
    """
    return service.register_to_picnic(picnic_id, user_id)

