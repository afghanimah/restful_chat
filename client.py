import requests
import hashlib
import json
import os

hosts = ["http://localhost:5000", "https://cool--server.herokuapp.com"]
host = ""
current_user = None
current_room = None

def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

def strict_input(message, valid_values, limit = None):
    """
    Block until valid_value is read from input.

    message:str - message to show
    valid_values:str list - list of valid strings
    limit:int - trys till timeout
    """
    result = None
    if limit != None: limit = -1 * abs(limit)

    while result not in valid_values and limit < 0:
        result = input(message)
        if limit != None: limit += 1
    
    if result not in valid_values:
        return None
    return result

def display():
    msg = """
    ==================================================
    {}
    --------------------------------------------------
    {}
    Capacity: {} / {}
    ==================================================
    """
    print(msg.format(current_room.get("name"), current_room.get("description"), len(current_room.get("users")), current_room.get("space")))

def show_messages(json):
    for m in json[-14:]:
        print("{}: {}".format(m.get("speaker"), m.get("message")))

def show_help():
    print("[@exit] or [@logout] exits")
    print("[@python *code*] executes python code")
    print("[@eval] evaluates expression")
    print("[@help] for help")

def logout():
    data = {
        "room_id": current_room.get("id"),
        "user_id": current_user.get("id")
    }
    requests.post(url = host + "/rooms/exit", json = data)

def is_command(msg):
    idx = msg.find(" ")
    if idx == -1:
        idx = len(msg)
    sub = msg[0:idx]
    if sub == "@exit" or sub == "@logout":
        logout()
        raise SystemExit
    elif sub == "@python":
        code = msg[idx+1:]
        exec(code)
    elif sub == "@eval":
        code = msg[idx+1:]
        print(eval(code))
    elif sub == "@help":
        show_help()
    else:
        return False
    return True

def update_room():
    global current_room
    r = requests.get(url = host + "/rooms/0")
    data = r.json()
    if data.get("room") == None:
        return
    current_room = data.get("room")

def chat():
    clear()
    display()
    while True:
        msg = input("> ")
        if is_command(msg):
            continue
        data = {
            "user": current_user.get("name"),
            "room_id": current_room.get("id"),
            "message": msg
        }
        r = requests.post(url = host + "/message", json = data)
        data = r.json()
        if data.get("success") == False:
            print("Failed to send")
        else:
            clear()
            update_room()
            display()
            show_messages(data.get("messages"))

def connect_hub_room():
    global current_room
    print("\nWelcome to the chat server {}!\nConnecting to the main room...".format(current_user.get("name")))
    r = requests.get(url = host + "/rooms/0")
    data = r.json()
    if data.get("room") == None:
        return False
    data = {
        "room_id": 0,
        "user_id": current_user.get("id")
    }
    r = requests.post(url = host + "/rooms/enter", json = data)
    data = r.json()
    if data.get("success") == False:
        return False
    print("Connected to main room!\n")
    current_room = data.get("room")
    return True

def register():
    global current_user
    username = input("Choose a username: ")
    password = input("Choose a password: ") + "salty salt"
    password = hashlib.sha256(password.encode()).hexdigest()
    data = {
        "username": username,
        "password": password
    }
    r = requests.put(url = host + "/register", json = data)
    data = r.json()
    current_user = data.get("user")
    return data.get("success") == True

def login():
    global current_user
    username = input("Username: ")
    password = input("Password: ") + "salty salt"
    password = hashlib.sha256(password.encode()).hexdigest()
    data = {
        "username": username,
        "password": password
    }
    r = requests.post(url = host + "/login", json = data)
    data = r.json()
    current_user = data.get("user")
    return data.get("success") == True

def connect():
    r = requests.post(url = host + "/connect")
    data = r.json()
    return data.get("success") == True

def setup_host_string():
    global host
    host_type = strict_input("Type [0] for localhost or \ntype [1] for live app: \n", ["0", "1"], 100)
    if host_type == None:
        return False
    host = hosts[int(host_type)]
    return True

def setup():
    print("Hello!  Welcome to the RESTful chat client!")
    print("This really should be implemented with sockets, but ehhh...")
    if not setup_host_string():
        print("Sorry, you tried too many times.  Please try again later")
        return
    print("\nConnecting to server...")

    if not connect():
        print("Could not connect, try again later.")
        return
    
    print("Connected to server!\n")

    reg_or_log = strict_input("Type [0] to register as a new user or \ntype [1] to login with existing account: \n", ["0", "1"], 100)
    result = None
    if reg_or_log == "0":
        result = register()
    elif reg_or_log == "1":
        result = login()
    else:
        print("Sorry, you tried too many times.  Please try again later")
        return
    
    if not result:
        print("Could not login, try again later.")
        return
    
    if not connect_hub_room():
        print("Could not connect to main room, try again later.")
        return
    
    chat()

if __name__ == '__main__':
    setup()