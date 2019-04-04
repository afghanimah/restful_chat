from base import Session, engine, Base
from user import User
from room import Room
from message import Message

def setup_db():
    Base.metadata.create_all(engine)

    session = Session()

    if session.query(User).first() == None:
        # plain text password: admin
        session.add(
            User(0, "admin", "103ed64fd2ec3a053dd50bca44ddf7ed6cdeedf83963c44044b494ea69afa52e")
        )
    if session.query(Room).first() == None:
        session.add(
            Room(0, "Main Room", "Initial room you connect to.", 100, "admin")
        )

    session.commit()
    session.close()

if __name__ == '__main__':
    setup_db()