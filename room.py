from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from base import Base

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    space = Column(Integer)
    admin = Column(String)
    users = relationship("User")
    chatbot = Column(Integer)

    def __init__(self, id, name, description, space, admin, password = None):
        self.id = id
        self.name = name
        self.description = description
        self.space = space
        self.admin = admin
        self.password = password
        self.users = []
        self.chatbot = None
    
    def to_dict(self):
        return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "space": self.space,
        "admin": self.admin,
        "users": [x.id for x in self.users]
        }