from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: int
    SECRET_KEY_JWT: str
    ALGORITHM_JWT: str
    TP_APP_ACCESS_TOKEN: str
    REGISTER_KEY: str

    class Config():
        env_file = '.env'


settings = Settings()
