from typing import Optional
import datetime as dt
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.util import greenlet_spawn

from python_test.database import get_db, get_async_db
from python_test.models.models import Picnic, User, City, PicnicRegistration
from python_test.models.schemas import PicnicAddResponse, PicnicRegistrationResponse, PicnicResponse


class PicnicService():
    def __init__(self, db: AsyncSession = Depends(get_async_db)) -> None:
        self.db = db

    async def all_picnics(self, datetime_: Optional[dt.datetime] = None, past: bool = True):
        query = select(Picnic)
        if datetime_ is not None:
            query = query.filter(Picnic.time == datetime_)
        if not past:
            query = query.filter(Picnic.time >= dt.datetime.now())
        res = await self.db.execute(query)
        picnics = res.scalars()
        result = []
        for picnic in picnics:
            city = await self.db.execute(select(City).where(City.id == picnic.city_id))
            city = city.scalar_one()
            users_list = list()
            for user in picnic.users:
                u = await self.db.execute(select(User).where(User.id == user.user_id))
                users_list.append(u.scalar_one())

            picnicDTO = PicnicResponse(
                id=picnic.id,
                city=city.name,
                time=picnic.time.strftime('%Y-%m-%dT%H:%M'),
                users=users_list
            )
            result.append(picnicDTO)

        return result

    def picnic_add(self, city_id: Optional[int] = None, datetime_: Optional[dt.datetime] = None):
        if city_id is None:
            raise HTTPException(status_code=400, detail='Параметр city_id должен быть указан')
        if datetime_ is None:
            raise HTTPException(status_code=400, detail='Параметр datetime должен быть указан')
        picnic = Picnic(city_id=city_id, time=datetime_)
        self.db.add(picnic)
        self.db.commit()

        result = PicnicAddResponse(
            id=picnic.id,
            city=self.db.query(City).get(picnic.city_id).name,
            time=picnic.time.strftime('%Y-%m-%dT%H:%M')
        )

        # return {
        #     'id': p.id,
        #     'city': Session().query(City).filter(City.id == p.id).first().name,
        #     'time': p.time,
        # }
        return result

    def register_to_picnic(self, picnic_id: Optional[int] = None, user_id: Optional[int] = None):
        """

        """
        if picnic_id is None:
            raise HTTPException(status_code=400, detail='Параметр picnic_id должен быть указан')
        if user_id is None:
            raise HTTPException(status_code=400, detail='Параметр user_id должен быть указан')
        try:
            user = self.db.query(User).get(user_id)
        except Exception:
            raise HTTPException(status_code=400, detail='Участник должен быть зарегистрирован')
        try:
            picnic = self.db.query(Picnic).get(picnic_id)
        except Exception:
            raise HTTPException(status_code=400, detail='Пикник должен быть зарегистрирован')

        picnic_reg = PicnicRegistration(
            user_id=user_id,
            picnic_id=picnic_id
        )
        self.db.add(picnic_reg)
        self.db.commit()

        result = PicnicRegistrationResponse(
            id=picnic_reg.id,
            user=user,
            picnic=PicnicAddResponse(
                id=picnic.id,
                city=self.db.query(City).get(picnic.city_id).name,
                time=picnic.time.strftime('%Y-%m-%dT%H:%M')
            )
        )
        return result
