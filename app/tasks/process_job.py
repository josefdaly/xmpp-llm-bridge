from redis_utils import redis_client, pull_job
from tasks.reply import process_messages_and_get_reply


def process_job():
    user_sender = pull_job(redis_client)
    if not user_sender:
        return None

    reply = process_messages_and_get_reply(user_sender, redis_client)
    if not reply:
        return
    return reply, user_sender
        
    
        