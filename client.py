from clientsetup import ClientSetup
from clientchat import ClientChat

if __name__ == '__main__':
    client_setup = ClientSetup()
    client_setup.setup()
    client_chat = ClientChat(client_setup)
    client_chat.chat()