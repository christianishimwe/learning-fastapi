from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_password: str
    access_token_expire_minutes: int
    secret_key: str
    algorithm: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
