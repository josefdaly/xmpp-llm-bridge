import pytest
from fakeredis import FakeRedis


from redis_utils import get_redis_client, set_message, get_messages, queue_job, pull_job


def test_set_and_get_message():
    # Use FakeRedis for testing
    fake_redis = FakeRedis()

    role_user = 'user'
    role_assistant = 'assistant'
    sender_user = 'user@domain'

    set_message("I need assistance with my account.", sender_user, role_user, fake_redis)
    set_message("Hello, how can I help you?", sender_user, role_assistant, fake_redis)
    set_message("I forgot my password.", sender_user, role_user, fake_redis)
    
    messages = get_messages(sender_user, fake_redis)
    expected = [
        {'role': 'user', 'content': 'I need assistance with my account.'},
        {'role': 'assistant', 'content': 'Hello, how can I help you?'},
        {'role': 'user', 'content': 'I forgot my password.'}
    ]
    assert messages == expected


def test_queue_and_pull_job():
    fake_redis = FakeRedis()

    sender_user1 = 'user1@domain'
    sender_user2 = 'user2@domain'

    queue_job(sender_user1, fake_redis)
    queue_job(sender_user2, fake_redis)

    pulled1 = pull_job(fake_redis)
    pulled2 = pull_job(fake_redis)
    pulled3 = pull_job(fake_redis)  # Should be None since queue is empty

    assert pulled1 == sender_user1
    assert pulled2 == sender_user2
    assert pulled3 is None