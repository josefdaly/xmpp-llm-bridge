import time
import xmpp

from tasks.process_job import process_job
from settings import XMPP_USER, XMPP_USER_PASSWORD, XMPP_SERVER



def main():
    client = xmpp.Client(XMPP_SERVER)
    client.connect(server=(XMPP_SERVER,5222))
    client.auth(XMPP_USER, XMPP_USER_PASSWORD, 'sender')
    client.sendInitPresence()

    while True:
        time.sleep(.5)
        reply_job = process_job()
        if reply_job:
            reply, user_sender = reply_job
            message = xmpp.Message(user_sender, reply)
            message.setAttr('type', 'chat')
            client.send(message)


if __name__ == "__main__":
    main()