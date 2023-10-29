import asyncio
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from python_test.models.schemas import CreateCityRequest
from python_test.models.models import City
from python_test.database import get_db, get_async_db
from python_test.models.schemas import City as CityDTO
from .external_requests import GetWeatherRequest


class CityService:
    def __init__(self, db: AsyncSession = Depends(get_async_db)) -> None:
        self.db = db

    async def create(self, data: Optional[CreateCityRequest]) -> CityDTO:
        if data is None:
            raise HTTPException(status_code=400, detail='The city parameter must be specified.')
        check = GetWeatherRequest()
        if not await check.check_existing(data.name):
            raise HTTPException(status_code=400, detail='The city parameter must be an existing city.')
        city = await self.db.execute(select(City).where(City.name == data.name.capitalize()))
        city = city.scalar_one_or_none()
        if city is None:
            city = City(name=data.name)
            self.db.add(city)
            await self.db.commit()
        weather = await city.weather
        return CityDTO(id=city.id, name=city.name, weather=weather)

    async def get_list(self, q: Optional[str] = None):
        query_set = select(City)
        if q is not None:
            query_set = query_set.filter(or_(City.name.like(f'%{q.lower()}%'), City.name.like(f'{q.title()}%')))
        result = await self.db.execute(query_set)
        cities = result.scalars()

        return [CityDTO(id=city.id, name=city.name, weather=await city.weather) for city in cities]