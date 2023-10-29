import json
from typing import Optional
import aiohttp
import aioredis

from python_test.settings import settings

WEATHER_API_KEY = '99ba78ee79a2a24bc507362c5288a81b'


class GetWeatherRequest():
    """
    Выполняет запрос на получение текущей погоды для города
    """

    # def __init__(self) -> None:
    #     """
    #     Инициализирует класс
    #     """
    #     self.session = requests.Session()

    async def get_weather_url(self, city: str) -> str:
        """
        Генерирует url включая в него необходимые параметры
        Args:
            city: Город
        Returns:

        """
        return f'https://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&appid={WEATHER_API_KEY}'

    async def send_request(self, url: str) -> aiohttp.ClientResponse:
        """
        Отправляет запрос на сервер
        Args:
            url: Адрес запроса
        Returns:

        """
        async with aiohttp.ClientSession() as session:
            r = await session.get(url)
        return r

    async def get_weather_from_response(self, response) -> float:
        """
        Достает погоду из ответа
        Args:
            response: Ответ, пришедший с сервера
        Returns:

        """
        if response.status != 200:
            response.raise_for_status()
        data = await response.text()
        data = json.loads(data)
        return data['main']['temp']

    async def get_weather(self, city: str) -> Optional[float]:
        """
        Делает запрос на получение погоды
        Args:
            city: Город
        Returns:

        """
        redis = await aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")

        cache = await redis.get(city)
        if cache is not None:
            return cache

        url = await self.get_weather_url(city)
        r = await self.send_request(url)
        if r is None:
            return None
        else:
            weather = await self.get_weather_from_response(r)

            await redis.set(city, weather, ex=3600)

            return weather

    async def check_existing(self, city: str) -> bool:
        """
        Проверяет наличие города
        Args:
            city: Название города
        Returns:

        """
        url = await self.get_weather_url(city)
        r = await self.send_request(url)
        if r.status == 404:
            return False
        if r.status == 200:
            return True
