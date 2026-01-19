from ollama import get_llm_reply, ROLE_ASSISTANT, ROLE_USER, ROLE_SYSTEM
from redis_utils import set_message, get_messages


def process_messages_and_get_reply(sender: str, redis_client) -> str:
    messages = get_messages(sender, redis_client)
    if not messages or messages[-1]['role'] != ROLE_USER:
        return
    response = get_llm_reply(messages, 75)
    response_json = response
    reply = response_json['message']['content']
    set_message(reply, sender, ROLE_ASSISTANT, redis_client)

    return reply
