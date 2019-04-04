from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

from base import Session
from user import User
from room import Room
from message import Message
import inserts

app = Flask(__name__)
CORS(app)

@app.route("/message", methods = ["POST"])
def send_message():
    session = Session()
    r = request.get_json(force=True)
    user = r.get("user")
    room_id = r.get("room_id")
    message = r.get("message")
    if message == None or message == "":
        session.close()
        return jsonify({"success": False})
    
    msg = Message(len(session.query(Message).all()), user, message, room_id, datetime.now())
    session.add(msg)
    session.commit()

    msgs = session.query(Message).filter(Message.room_id == room_id).all()
    msgs = [x.to_dict() for x in msgs]

    session.close()
    return jsonify({"messages": msgs})

@app.route("/rooms/enter", methods = ["POST"])
def enter_room():
    session = Session()
    r = request.get_json(force=True)
    user_id = r.get("user_id")
    room_id = r.get("room_id")

    r = session.query(Room).filter(Room.id == room_id).first()
    u = session.query(User).filter(User.id == user_id).first()
    if r == None or u == None:
        session.close()
        return jsonify({"success": False})
    elif len(r.users) >= r.space:
        session.close()
        return jsonify({"success": False})
    r.users.append(u)
    room = r.to_dict()
    session.commit()
    session.close()
    return jsonify({"room": room})

@app.route("/rooms/exit", methods = ["POST"])
def exit_room():
    session = Session()
    r = request.get_json(force=True)
    user_id = r.get("user_id")
    room_id = r.get("room_id")

    r = session.query(Room).filter(Room.id == room_id).first()
    u = session.query(User).filter(User.id == user_id).first()
    if r == None or u == None:
        session.close()
        return jsonify({"success": False})
    elif len(r.users) >= r.space:
        session.close()
        return jsonify({"success": False})
    r.users.remove(u)

    session.commit()
    session.close()
    return jsonify({"success": True})

@app.route("/rooms/<int:room_id>", methods = ["GET"])
def get_room(room_id):
    session = Session()
    r = session.query(Room).filter(Room.id == room_id).first()
    if r == None:
        session.close()
        return jsonify({"room": None})
    r = r.to_dict()
    session.close()
    return jsonify({"room": r})

@app.route("/users/<int:user_id>", methods = ["GET"])
def get_user(user_id):
    session = Session()
    u = session.query(User).filter(User.id == user_id).first()
    if u == None:
        session.close()
        return jsonify({"user": None})
    user = u.to_dict()
    session.close()
    return jsonify({"user": user})

@app.route("/register", methods = ["PUT"])
def register():
    session = Session()
    r = request.get_json(force=True)
    un = r.get("username")
    pw = r.get("password")

    u = session.query(User).filter(User.name == un).all()
    if len(u) > 0:
        session.close()
        return jsonify({"success": False})
    
    u = User(len(session.query(User).all()),un, pw)
    session.add(u)
    user = u.to_dict()
    session.commit()
    session.close()
    return jsonify({"success": True, "user": user})

@app.route("/login", methods = ["POST"])
def login():
    session = Session()
    r = request.get_json(force=True)
    un = r.get("username")
    pw = r.get("password")

    u = session.query(User).filter(User.name == un and User.password == pw).all()
    if len(u) != 1:
        session.close()
        return jsonify({"success": False})
    user = u[0].to_dict()
    session.close()
    return jsonify({"success": True, "user": user})

@app.route("/connect", methods = ["POST"])
def connect():
    return jsonify({"success": True})

if __name__ == '__main__':
    inserts.setup_db()
    app.run(debug=True)