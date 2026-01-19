import pytest
from fakeredis import FakeRedis

from tasks.reply import process_messages_and_get_reply, set_message, get_messages
from ollama import ROLE_ASSISTANT, ROLE_USER
from settings import OLLAMA_BASE_URL

def setup_function():
    global fake_redis, sender
    fake_redis = FakeRedis()
    sender = 'user@domain'

def test_process_messages_and_get_reply(requests_mock):
    set_message("I need assistance with my account.", sender, ROLE_USER, fake_redis)
    set_message("Hello, how can I help you?", sender, ROLE_ASSISTANT, fake_redis)
    set_message("I forgot my password.", sender, ROLE_USER, fake_redis)

    mock_response = {"message": {"content": "Sure, I can help you reset your password."}}
    requests_mock.post(f"{OLLAMA_BASE_URL}/api/chat", json=mock_response, status_code=200)

    reply = process_messages_and_get_reply(sender, fake_redis)

    assert reply == "Sure, I can help you reset your password."

    messages = get_messages(sender, fake_redis)
    expected = [
        {'role': ROLE_USER, 'content': 'I need assistance with my account.'},
        {'role': ROLE_ASSISTANT, 'content': 'Hello, how can I help you?'},
        {'role': ROLE_USER, 'content': 'I forgot my password.'},
        {'role': ROLE_ASSISTANT, 'content': 'Sure, I can help you reset your password.'}
    ]
    assert messages == expected


def test_process_messages_no_messages(requests_mock):
    messages = get_messages(sender, fake_redis)
    assert messages == []

    # should not get here
    mock_response = {"message": {"content": "Sure, I can help you reset your password."}}
    requests_mock.post(f"{OLLAMA_BASE_URL}/api/chat", json=mock_response, status_code=200)

    reply = process_messages_and_get_reply(sender, fake_redis)
    assert reply is None


def test_process_messages_last_not_user(requests_mock):
    set_message("I need assistance with my account.", sender, ROLE_USER, fake_redis)
    set_message("Hello, how can I help you?", sender, ROLE_ASSISTANT, fake_redis)

    # should not get here
    mock_response = {"message": {"content": "Sure, I can help you reset your password."}}
    requests_mock.post(f"{OLLAMA_BASE_URL}/api/chat", json=mock_response, status_code=200)

    reply = process_messages_and_get_reply(sender, fake_redis)
    assert reply is None