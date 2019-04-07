import requests
import hashlib
import getpass

def strict_input(message, valid_values, limit = None):
        """
        Block until valid_value is read from input.

        message:str - message to show
        valid_values:str list - list of valid strings
        limit:int - trys till timeout
        """
        result = None

        while result not in valid_values and (limit == None or limit < 0):
            result = input(message)
            if limit != None: limit -= 1
        
        if result not in valid_values:
            return None
        return result

class ClientSetup():
    hosts = ["http://localhost:5000", "https://cool--server.herokuapp.com"]

    def __init__(self):
        self.host = ""
        self.current_user = None
        self.current_room = None
        self.setup_success = None

    def __connect_hub_room(self):
        print("\nWelcome to the chat server, {}!\nConnecting to the main room...".format(self.current_user.get("name")))
        data = {
            "room_id": 0,
            "user_id": self.current_user.get("id")
        }
        r = requests.post(url = self.host + "/rooms/enter", json = data)
        data = r.json()
        if data.get("success") == False:
            return False
        print("Connected to main room!\n")
        self.current_room = data.get("room")
        return True

    def __register(self):
        username = input("Choose a username: ")
        password = input("Choose a password: ") + "salty salt"
        password = hashlib.sha256(password.encode()).hexdigest()
        data = {
            "username": username,
            "password": password
        }
        r = requests.put(url = self.host + "/register", json = data)
        data = r.json()
        self.current_user = data.get("user")
        return data.get("success") == True

    def __login(self):
        username = input("Username: ")
        password = getpass.getpass("Password: ") + "salty salt"
        password = hashlib.sha256(password.encode()).hexdigest()
        data = {
            "username": username,
            "password": password
        }
        r = requests.post(url = self.host + "/login", json = data)
        data = r.json()
        self.current_user = data.get("user")
        return data.get("success") == True

    def __connect(self):
        r = requests.post(url = self.host + "/connect")
        data = r.json()
        return data.get("success") == True

    def __setup_host_string(self):
        host_type = strict_input("Type [0] for localhost or \ntype [1] for live app: \n", ["0", "1"], 100)
        if host_type == None:
            return False
        self.host = ClientSetup.hosts[int(host_type)]
        return True

    def setup(self):
        print("Hello!  Welcome to the RESTful chat client!")
        print("This really should be implemented with sockets, but ehhh...")
        if not self.__setup_host_string():
            print("Sorry, you tried too many times.  Please try again later")
            self.setup_success = False
            return self.setup_success
        print("\nConnecting to server...")

        if not self.__connect():
            print("Could not connect, try again later.")
            self.setup_success = False
            return self.setup_success
        print("Connected to server!\n")

        reg_or_log = strict_input("Type [0] to register as a new user or \ntype [1] to login with existing account: \n", ["0", "1"], 100)
        result = None
        if reg_or_log == "0":
            result = self.__register()
        elif reg_or_log == "1":
            result = self.__login()
        else:
            print("Sorry, you tried too many times.  Please try again later")
            self.setup_success = False
            return self.setup_success
        
        if not result:
            print("Could not login, try again later.")
            self.setup_success = False
            return self.setup_success
        if not self.__connect_hub_room():
            print("Could not connect to main room, try again later.")
            self.setup_success = False
            return self.setup_success
        self.setup_success = True
        return self.setup_success