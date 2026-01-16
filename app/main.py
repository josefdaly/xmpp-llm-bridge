import xmpp
from ollama import get_llm_reply
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
        if not msg:
            return
        # try:
        llm_reply = get_llm_reply(msg, message.getFrom())
        # except Exception as e:
        #     llm_reply = "Sorry, I'm having trouble connecting to the LLM service."
        reply = xmpp.Message(message.getFrom(), llm_reply)
        reply.setAttr('type', 'chat')
        conn.send(reply)


if __name__ == "__main__":
    main()
