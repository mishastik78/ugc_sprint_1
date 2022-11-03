from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_client_id: str
    kafka_instance: str
    kafka_topic_name: str
    kafka_timeout_ms: int
    kafka_max_messages: int
    clickhouse_host: str
    backoff_max_retries: int = 10
    backoff_initial_sec: float = 2
    backoff_max_sec: float = 600

    class Config:
        env_file = '.env'


settings = Settings()
