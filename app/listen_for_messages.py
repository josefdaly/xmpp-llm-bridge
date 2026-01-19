import xmpp

from redis_utils import redis_client, set_message, queue_job
from ollama import ROLE_USER
from settings import XMPP_USER, XMPP_USER_PASSWORD, XMPP_SERVER


def main():
    client = xmpp.Client(XMPP_SERVER)
    client.connect(server=(XMPP_SERVER,5222))
    client.auth(XMPP_USER, XMPP_USER_PASSWORD, 'botty')
    client.sendInitPresence()
    client.RegisterHandler('message', messageCB)
    # Start the main loop to listen for events
    print("Bot is running and listening for messages...")
    while True:
        client.Process(1) # Process events for 1 second


def messageCB(conn, message):
    print(f"Received from: {message.getFrom()}")
    print(f"Message Body: {message.getBody()}")
    # You can add logic here to process the message, e.g., reply
    if message.getType() == 'chat':
        msg = message.getBody()
        user_sender = message.getFrom()

        set_message(msg, user_sender, ROLE_USER, redis_client)
        queue_job(user_sender, redis_client)


if __name__ == "__main__":
    main()
