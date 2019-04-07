import requests
import os

class ClientChat():
    def __init__(self, client_setup):
        if client_setup.setup_success != True:
            raise Exception("client_setup should have been successfully setup.")
        
        self.host = client_setup.host
        self.current_user = client_setup.current_user
        self.current_room = client_setup.current_room
        self.local_msgs = []
        self.current_msg = ""

    def clear(self):
        _ = os.system("cls||clear")

    def show_messages(self, json):
        for m in json[-14:]:
            print("{}: {}".format(m.get("speaker"), m.get("message")))

    def update_screen(self):
        self.clear()
        msg = """
        ==================================================
        {}
        --------------------------------------------------
        {}
        Capacity: {} / {}
        ==================================================
        """
        print(msg.format(self.current_room.get("name"), self.current_room.get("description"), len(self.current_room.get("users")), self.current_room.get("space")))

    def show_help(self):
        print("[@exit] or [@logout] exits")
        print("[@python *code*] executes python code")
        print("[@eval] evaluates expression")
        print("[@help] for help")

    def logout(self):
        data = {
            "room_id": self.current_room.get("id"),
            "user_id": self.current_user.get("id")
        }
        requests.post(url = self.host + "/rooms/exit", json = data)

    def is_command(self, msg):
        idx = msg.find(" ")
        if idx == -1:
            idx = len(msg)
        sub = msg[0:idx]
        if sub == "@exit" or sub == "@logout":
            self.logout()
            raise SystemExit
        elif sub == "@python":
            code = msg[idx+1:]
            exec(code)
        elif sub == "@eval":
            code = msg[idx+1:]
            print(eval(code))
        elif sub == "@help":
            self.show_help()
        else:
            return False
        return True

    def update_room(self):
        r = requests.get(url = self.host + "/rooms/0")
        data = r.json()
        if data.get("room") == None:
            return
        self.current_room = data.get("room")

    def chat(self):
        self.update_screen()
        while True:
            msg = input("> ")
            if self.is_command(msg):
                continue
            data = {
                "user": self.current_user.get("name"),
                "room_id": self.current_room.get("id"),
                "message": msg
            }
            r = requests.post(url = self.host + "/messages", json = data)
            data = r.json()
            if data.get("success") == False:
                print("Failed to send")
            else:
                self.update_room()
                self.update_screen()
                self.show_messages(data.get("messages"))