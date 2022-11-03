import logging
import time

from clickhouse_driver.errors import NetworkError

from config import settings


def backoff(func):
    def wrapper(*args, **kwargs):
        max_retries: int = settings.backoff_max_retries
        initial_backoff: float = settings.backoff_initial_sec
        max_backoff: float = settings.backoff_max_sec
        for attempt in range(max_retries + 1):
            if attempt:
                logging.debug('Connection attempt %s', attempt)
                time.sleep(min(max_backoff, initial_backoff * 2 ** (attempt - 1)))
            try:
                func(*args, **kwargs)
            except NetworkError as e:
                logging.exception(e)
                if attempt == max_retries:
                    raise
            else:
                break

    return wrapper
