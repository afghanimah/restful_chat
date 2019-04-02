from app_base import Session, engine, Base
from user import User
from room import Room
from message import Message

Base.metadata.create_all(engine)

session = Session()

admin = User(0, "admin", "103ed64fd2ec3a053dd50bca44ddf7ed6cdeedf83963c44044b494ea69afa52e")
hub = Room(0, "Main Room", "Initial room you connect to.", 100, "admin")

session.add(admin)
session.add(hub)

session.commit()
session.close()