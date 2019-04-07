import requests
import os
from threading import Thread
import kbhit
import terminalsize
import time

def fast_string_concat(string_list, delimiter=""):
    return delimiter.join([repr(s) for s in string_list])

def dummy_msg(speaker, msg):
    return {
        "speaker": speaker,
        "message": msg
    }

class ClientChat():
    def __init__(self, client_setup):
        if client_setup.setup_success != True:
            raise Exception("client_setup should have been successfully setup.")
        
        self.host = client_setup.host
        self.current_user = client_setup.current_user
        self.current_room = client_setup.current_room
        self.local_msgs = []
        self.current_msg = ""
        self.last_msg_id = -1
        self.last_msg_len = 0
        self.server_watcher = Thread(target = self.watchServer)
        self.done = False
        _, h = terminalsize.get_terminal_size()
        self.height = int(h* 0.4)

    def clear(self):
        _ = os.system("cls||clear")
    
    def watchServer(self):
        while not self.done:
            new_msgs = self.get_new_messages_id(self.last_msg_id)
            new_room = self.update_room()
            if new_msgs or new_room:
                self.update_screen()
            time.sleep(3)
            

    def show_messages(self):
        for m in self.local_msgs[-1 * self.height:]:
            print("{}: {}".format(m.get("speaker"), repr(m.get("message"))[1:-1]))

    def update_screen(self):
        self.clear()
        ui = """
        ==================================================
        {}
        --------------------------------------------------
        {}
        Capacity: {} / {}
        ==================================================
        """
        print(ui.format(self.current_room.get("name"), self.current_room.get("description"), len(self.current_room.get("users")), self.current_room.get("space")))
        self.show_messages()
        print("> {}".format(self.current_msg), end="", flush=True)

    def show_help(self):
        self.local_msgs.append(dummy_msg("Server", "[@exit] or [@logout] or ESC 2 times exits"))
        self.local_msgs.append(dummy_msg("", "[@python *code*] executes python code"))
        self.local_msgs.append(dummy_msg("", "[@eval] evaluates expression"))
        self.local_msgs.append(dummy_msg("", "[@help] for help"))

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
            self.local_msgs.append(dummy_msg(self.current_user.get("name"), msg))
            self.local_msgs.append(dummy_msg("Server", "Logging out..."))
            self.done = True
        elif sub == "@python":
            self.local_msgs.append(dummy_msg(self.current_user.get("name"), msg))
            code = msg[idx+1:]
            result = ""
            try:
                result = exec(code)
            except:
                result = "Exception"
            self.local_msgs.append(dummy_msg("Server", "Result: " + str(result)))
        elif sub == "@eval":
            self.local_msgs.append(dummy_msg(self.current_user.get("name"), msg))
            code = msg[idx+1:]
            result = eval(code)
            self.local_msgs.append(dummy_msg("Server", "Result: " + str(result)))
        elif sub == "@help":
            self.local_msgs.append(dummy_msg(self.current_user.get("name"), msg))
            self.show_help()
        else:
            return False
        return True

    def update_room(self):
        r = requests.get(url = self.host + "/rooms/0")
        data = r.json()
        if data.get("room") == None:
            return False
        room = data.get("room")
        if len(room.get("users")) != len(self.current_room.get("users")):
            self.current_room = room
            return True
        return False
    
    def get_new_messages_id(self, id):
        r = requests.get(url = self.host + "/messages/{}/id/{}".format(0, str(id)))
        data = r.json()
        for m in data.get("messages"):
            self.local_msgs.append(m)
            self.last_msg_id = max(self.last_msg_id, int(m.get("id")))
        if id != self.last_msg_id or self.last_msg_len != len(self.local_msgs):
            self.last_msg_len = len(self.local_msgs)
            return True
        return False
    
    def get_new_messages_limit(self, limit):
        r = requests.get(url = self.host + "/messages/{}/limit/{}".format(0, limit))
        data = r.json()
        for m in data.get("messages"):
            print(m)
            self.local_msgs.append(m)
            self.last_msg_id = max(self.last_msg_id, m.get("id"))

    def chat(self):
        self.get_new_messages_limit(self.height)
        self.update_screen()
        kb = kbhit.KBHit()
        self.server_watcher.start()
        last_escape = False

        while not self.done:
            c = kb.getch()
            if c == "\n" and self.current_msg != "":
                if self.is_command(self.current_msg):
                    self.current_msg = ""
                else:
                    data = {
                        "user": self.current_user.get("name"),
                        "room_id": self.current_room.get("id"),
                        "message": self.current_msg
                    }
                    r = requests.post(url = self.host + "/messages", json = data)
                    data = r.json()
                    if data.get("success") == False:
                        self.local_msgs.append("Failed to send message")
                    else:
                        self.current_msg = ""
                last_escape = False
            elif c == "\x1b":
                if last_escape:
                    self.done = True
                    self.logout()
                else:
                    last_escape = True
                    self.current_msg += repr(c)[1:-1]
            elif c == "\x7f":
                last_escape = False
                self.current_msg = self.current_msg[:-1]
            else:
                last_escape = False
                self.current_msg += repr(c)[1:-1]
            self.update_screen()
        
        kb.set_normal_term()
        self.server_watcher.join()