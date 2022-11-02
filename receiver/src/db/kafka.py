from functools import lru_cache

from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None = None


@lru_cache()
def get_producer():
    return producer
