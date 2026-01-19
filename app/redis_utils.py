import redis
import json

from utils import format_message
from settings import REDIS_HOST, REDIS_PORT


def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def set_message(message: str, user_sender: str, role: str, redis_client) -> str:
    msg = format_message(message, role)
    redis_client.rpush(str(user_sender), str(json.dumps(msg)))


def queue_job(user_sender: str, redis_client) -> None:
    redis_client.rpush("reply_queue", str(user_sender))


def pull_job(redis_client) -> str:
    user_sender = redis_client.lpop("reply_queue")
    if user_sender:
        return user_sender.decode('utf-8')


def get_messages(user_sender: str, redis_client) -> list[str]:
    messages = redis_client.lrange(str(user_sender), 0, -1)
    return [json.loads(msg.decode('utf-8')) for msg in messages]


redis_client = get_redis_client()