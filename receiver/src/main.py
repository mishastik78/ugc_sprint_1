import asyncio

import uvicorn as uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import receiver
from core.config import get_settings
from db import kafka

settings = get_settings()

loop = asyncio.get_event_loop()
app = FastAPI(
    title=settings.app_name,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup_event():
    kafka.producer = AIOKafkaProducer(
        loop=loop,
        client_id=settings.kafka_client_id,
        bootstrap_servers=settings.kafka_instance
    )
    await kafka.producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka.producer.stop()


app.include_router(receiver.router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
