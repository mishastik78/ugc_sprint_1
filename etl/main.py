from time import sleep

import clickhouse_driver
import kafka

from config import Settings

settings = Settings()
consumer = kafka.KafkaConsumer(
    settings.kafka_topic_name,
    client_id=settings.kafka_name,
    bootstrap_servers=settings.kafka_instance,
    group_id='etl',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    consumer_timeout_ms=settings.kafka_timeout_ms,
)
clickhouse = clickhouse_driver.Client(host=settings.clickhouse_host)


def read_kafka():
    for msg in consumer:
        user, _, film = msg.key.partition('+')
        yield user, film, msg.value


def proceed():
    while True:
        payload: list(tuple) = []
        count: int = 0
        for user_id, film_id, time in read_kafka():
            payload.append(tuple(user_id, film_id, time))
            count += 1
            if count > settings.kafka_max_messages:
                break
        if payload:
            clickhouse.execute('INSERT INTO film_views (user_id, film_id, timestamp) VALUES (%s, %s, %s)', payload)
            consumer.commit()
            del payload
        else:
            sleep(1)


if __name__ == '__main__':
    clickhouse.execute('CREATE DATABASE IF NOT EXISTS db ON CLUSTER company_cluster')
    clickhouse.execute(
        '''CREATE TABLE IF NOT EXISTS db.film_views 
        ON CLUSTER company_cluster (user_id String, film_id String, timestamp DateTime) 
        Engine=MergeTree() ORDER BY user_id'''
    )
    proceed()
