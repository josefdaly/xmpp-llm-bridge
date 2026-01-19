import redis
import json

from utils import format_message
from settings import REDIS_HOST, REDIS_PORT

def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def set_message(message: str, user_sender: str, role: str, redis_client) -> str:
    msg = format_message(message, role)
    redis_client.rpush(str(user_sender), str(json.dumps(msg)))


def get_messages(sender: str, redis_client) -> list[str]:
    messages = redis_client.lrange(str(sender), 0, -1)
    return [json.loads(msg.decode('utf-8')) for msg in messages]
