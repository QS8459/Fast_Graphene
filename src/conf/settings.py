from pydantic_settings import BaseSettings
from pydantic import Extra


class Settings(BaseSettings):
    db: str
    app_title: str
    app_version: str
    app_description: str
    token_exp_time_sec: int
    refresh_token_exp_time_sec:int
    token_key: str
    token_alg: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = Extra.allow
        env_prefix = "GQ_"


settings = Settings()
