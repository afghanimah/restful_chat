from sqlalchemy import Column, String, Integer, ForeignKey
from base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    status = Column(Integer)
    location_id = Column(Integer, ForeignKey("rooms.id"))
    location = Column(String)

    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
        self.status = 0
        self.location = ""
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "location": self.location
        }