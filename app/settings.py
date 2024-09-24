import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = 'root'
    POSTGRES_PASSWORD: str = 'root'
    POSTGRES_DB: str = 'db'
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "app.log"

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"


settings = Settings()


logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=settings.LOG_FILE_PATH,
    filemode='a'
)

logger = logging.getLogger(__name__)
