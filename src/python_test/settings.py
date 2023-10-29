from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    The Settings class inherits from the parent BaseSettings class from the pydantic_settings module.
    Contains the necessary settings for working with the database.
    """
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    redis_host: str
    redis_port: int

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        # DSN
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self) -> str:
        # DSN
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file='../../.env')


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
