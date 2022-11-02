from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_client_id: str
    kafka_instance: str
    kafka_topic_name: str
    kafka_timeout_ms: int
    kafka_max_messages: int
    clickhouse_host: str

    class Config:
        env_file = '.env'
