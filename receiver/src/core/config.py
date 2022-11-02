from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Player timestamp receiver'
    docs_url: str = '/api/openapi'
    openapi_url: str = '/api/openapi.json'
    kafka_client_id: str
    kafka_instance: str
    kafka_topic_name: str
    auth_url: str

    class Config:
        env_file = '.env'


@lru_cache
def get_settings():
    return Settings()
