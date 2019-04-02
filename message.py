from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    speaker = Column(String)
    message = Column(String)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("Room")
    time = Column(DateTime)

    def __init__(self, id, speaker, message, room_id, time):
        self.id = id
        self.speaker = speaker
        self.message = message
        self.room_id = room_id
        self.time = time
    
    def to_dict(self):
        return {
            "id": self.id,
            "speaker": self.speaker,
            "message": self.message,
            "room_id": self.room_id,
            "time": self.time
        }

def generate_message(dict):
    return Message(
        dict.get("id"),
        dict.get("speaker"),
        dict.get("message"),
        dict.get("room_id"),
        dict.get("time")
    )