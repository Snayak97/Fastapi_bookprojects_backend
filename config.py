from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    JWT_SECRET_KEY : str
    JWT_ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES :int
    REFRESS_TOKEN_EXPIRE_DAYS :int

    REDIS_HOST : str = "127.0.0.1"
    REDIS_PORT : int = 6379

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")



Config = Settings()