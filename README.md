# Hello!
This is a set of 2 scripts.  The server and client files.  The server file is running on a host and the client is what you will be running on your machine.

This project is a client/server project made for fun, however if was implemented using a RESTful design rather than with sockets.  Since this is a chatting app, using sockets would be much MUCH better, but ehhhhhh... I didn't care as much about efficiency as much as figuring out how to setup a database on the host.  I could have done a different project that made more sense with REST, but this seemed like more fun than a generic CRUD system.

# Instructions for Setting up Client app
Note: these instructions were only tested for MacOS

## Requirements:
- python3
- pip
    - https://pip.pypa.io/en/stable/installing/
- some sort of virual environment:
    - pip package: https://virtualenv.pypa.io/en/latest/installation/
    - venv from python3 (should already be installed)
    - any others

## Setup
Note: if you get any sort of SSL errors, look here:
https://stackoverflow.com/questions/49768770/not-able-to-install-python-packages-ssl-tlsv1-alert-protocol-version

1. create virtual environment (example from python3 venv)

    `python3 -m venv venv`
2. start virtual environment

    `. venv/bin/activate`

    if you want to leave the virutal environment: `deactivate`
2. install requirements

    `pip install -r requirements.txt`

## Start
All you need to do is run the client.py script from inside the virtual environment

`python3 client.py`

You will first be asked for a connection type.  Unless you are running the server on your **localhost**, choose the **live app**.

After establishing that the server is online, you will be asked to **register** or **login**.  If you have an account you can reuse it, otherwise make a new one.  You will be asked for your *Username* and *Password* after choosing.

If you successfully connected to the server, then you will be put into the **Main Room**.  There is only 1 room at this time.

Now you can type a message and send it to other users.  Due to the RESTful nature of the system (not using sockets), you will only get updated information when you send a new message.

Type `@help` to get a list of commands:
- `@exit` or `@logout` to logout of the server
- `@python x=[4,5]; print(len(x)*4*5)` to execute sample python code
- `@eval 3+4` to evaluate math expressions

## Known Bugs
- If you don't use `@exit` or `@logout` to logout, user will stay logged in on server.

    And probably a lot more I haven't run into yet.

# Instructions for Running Server on localhost

## Setup and Requirements
The set up and requirements are the same for the client app

You will need to change the BACKUP_DATABASE_URL in base.py to your database connection string

If you like, you can run inserts.py from the virtual environment, but it should automatically run after starting the server app:

`python3 inserts.py`

The admin account has no special permissions, so that's why the password is sitting in the file.  Password for admin: *admin*

That should be it for localhost setup for the server

## Start
All you need to do is run the server.py script from inside the virtual environment

`python3 server.py`

The terminal will then block while executing the Flask app

You can now open other terminals to run clients to connect via **localhost**