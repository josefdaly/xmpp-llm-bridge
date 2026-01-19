import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6380))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
XMPP_USER = os.getenv("XMPP_USER")
XMPP_USER_PASSWORD = os.getenv("XMPP_USER_PASSWORD")
XMPP_SERVER = os.getenv("XMPP_SERVER")
MODEL_NAME = os.getenv("MODEL_NAME")