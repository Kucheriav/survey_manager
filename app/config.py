import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    SECRET_KEY: str
    SECURITY_PASSWORD_SALT: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    UPLOAD_FOLDER: str
    MAX_CONTENT_LENGTH: int
    ALLOWED_EXTENSIONS_STR: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    API_KEY: str


    # файл .env должен лежать в папке самого проекта survey_manager (на уровень выше)
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    )

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

config = Config()
