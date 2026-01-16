import requests

from settings import OLLAMA_BASE_URL
from redis_utils import set_message, get_messages


ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"


def get_tags():
    response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
    return response.json()


def pull_model(model_name: str):
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/pull",
        json={
            "model": model_name,
            "stream": False,
        },
    )
    return response.json()


def get_llm_reply(prompt: str, sender: str) -> str:
    print(prompt)
    print(sender)
    set_message(prompt, sender, ROLE_USER)
    messages = get_messages(sender)
    
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": "gemma3",
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": 100
            }     
        },
    )
    response_json = response.json()
    reply = response_json['message']['content']
    set_message(reply, sender, ROLE_ASSISTANT)

    return reply
