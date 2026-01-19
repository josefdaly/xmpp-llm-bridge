from ollama import get_llm_reply, ROLE_ASSISTANT, ROLE_USER, ROLE_SYSTEM
from redis_utils import set_message, get_messages


def consume_and_process_message(prompt: str, sender: str) -> str:
    set_message(prompt, sender, ROLE_USER)
    messages = get_messages(sender)

    response = get_llm_reply(messages, 75)

    response_json = response
    reply = response_json['message']['content']
    set_message(reply, sender, ROLE_ASSISTANT)

    return reply
