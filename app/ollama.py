import requests

from settings import OLLAMA_BASE_URL, MODEL_NAME


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
    response.raise_for_status()
    return response.json()


def get_llm_reply(messages: list, token_limit: int) -> str:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": token_limit
            }     
        },
    )
    response.raise_for_status()
    return response.json()
