from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Header, HTTPException, Depends
from httpx import AsyncClient

from core.config import Settings, get_settings
from db.kafka import get_producer
from .model import Message

router = APIRouter()


async def auth(authorization: str | None = Header(default=None), settings: Settings = Depends(get_settings)) -> str:
    """Передаем токен как есть в службу авторизации и получаем id пользователя"""
    async with AsyncClient() as client:
        response = await client.get(settings.auth_url, headers={'Authorization': authorization})
        if response.status_code != 200:
            # В случае ошибки отдаем ее как есть
            raise HTTPException(
                status_code=response.status_code, detail=response.content
            )
        return response.json().get('id')


@router.post('/receiver', status_code=200)
async def get_timestamp(
        msg: Message,
        user_id: str = Depends(auth),
        producer: AIOKafkaProducer = Depends(get_producer),
        settings: Settings = Depends(get_settings),
):
    await producer.send(
        topic=settings.kafka_topic_name,
        value=msg.timestamp,
        key=f'{user_id}+{msg.film_id}'
    )
    return {}
