from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    database_url: str
    database_name: str

    redis_url: str
    cache_expire: int

    jwt_secret: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()