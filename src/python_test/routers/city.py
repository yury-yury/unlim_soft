from typing import List, Optional

from fastapi import APIRouter, Query, Body, Depends

from python_test.services.city import CityService
from python_test.models.schemas import CreateCityRequest
from python_test.models.schemas import City as CityDTO


city_router = APIRouter()


@city_router.post('/create/',
                  summary='Create City',
                  description='Creation of a city by its name',
                  response_model=CityDTO)
async def create_city(data: CreateCityRequest = Body(description="Название города", default=None),
                      service: CityService = Depends()) -> CityDTO:
    return await service.create(data)


@city_router.get('/list/',
                 summary='Get list of Cities',
                 description='Displaying a list of cities available in the database.',
                 response_model=List[CityDTO])
async def cities_list(q: Optional[str] = Query(description="Substring from city name.", default=None),
                      service: CityService = Depends()) -> List[CityDTO]:
    """
    Получение списка городов
    """
    return await service.get_list(q)
