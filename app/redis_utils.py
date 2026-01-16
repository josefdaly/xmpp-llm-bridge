import redis
import json

from settings import REDIS_HOST, REDIS_PORT

def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def format_message(prompt: str, role: str) -> str:
    return {"role": role, "content": prompt}


def set_message(message: str, sender: str, role: str) -> str:
    redis_client = get_redis_client()
    msg = format_message(message, role)
    redis_client.rpush(sender, json.dumps(msg))


def get_messages(sender: str) -> list[str]:
    redis_client = get_redis_client()
    messages = redis_client.lrange(sender, 0, -1)
    return [json.loads(msg.decode('utf-8')) for msg in messages]