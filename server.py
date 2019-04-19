from flask import Flask, jsonify, request, g
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import desc

from database.base import Session
from models.user import User
from models.room import Room
from models.message import Message
import database.inserts as inserts

app = Flask(__name__)
CORS(app)

@app.before_request
def create_session():
    g.session = Session()

@app.teardown_appcontext
def shutdown_session(response_or_exception=None):
    if hasattr(g, "session"):
        g.session.commit()
        g.session.close()

@app.route("/messages/<int:room_id>/id/<int:msg_id>", methods = ["GET"])
def get_all_messages_after_id(room_id, msg_id):
    msgs = g.session.query(Message).filter((Message.room_id == room_id) & (Message.id > msg_id)).all()
    msgs = [x.to_dict() for x in msgs]
    return jsonify({"messages": msgs})

@app.route("/messages/<int:room_id>/limit/<int:num>", methods = ["GET"])
def get_all_messages_limit(room_id, num):
    msgs = g.session.query(Message).filter(Message.room_id == room_id).order_by(Message.id.desc()).limit(num)
    msgs = msgs[::-1]
    msgs = [x.to_dict() for x in msgs]
    return jsonify({"messages": msgs})

@app.route("/messages/<int:room_id>", methods = ["GET"])
def get_all_messages(room_id):
    msgs = g.session.query(Message).filter(Message.room_id == room_id).all()
    msgs = [x.to_dict() for x in msgs]
    return jsonify({"messages": msgs})

@app.route("/messages", methods = ["POST"])
def send_message():
    r = request.get_json(force=True)
    user = r.get("user")
    room_id = r.get("room_id")
    message = r.get("message")
    if message == None or message == "":
        return jsonify({"success": False})
    
    msg = Message(len(g.session.query(Message).all()), user, message, room_id, datetime.now())
    g.session.add(msg)
    return jsonify({"success": True})

@app.route("/rooms/enter", methods = ["POST"])
def enter_room():
    r = request.get_json(force=True)
    user_id = r.get("user_id")
    room_id = r.get("room_id")

    r = g.session.query(Room).filter(Room.id == room_id).first()
    u = g.session.query(User).filter(User.id == user_id).first()
    if r == None or u == None:
        return jsonify({"success": False})
    elif len(r.users) >= r.space:
        return jsonify({"success": False})
    r.users.append(u)
    room = r.to_dict()
    return jsonify({"room": room})

@app.route("/rooms/exit", methods = ["POST"])
def exit_room():
    r = request.get_json(force=True)
    user_id = r.get("user_id")
    room_id = r.get("room_id")

    r = g.session.query(Room).filter(Room.id == room_id).first()
    u = g.session.query(User).filter(User.id == user_id).first()
    if r == None or u == None:
        return jsonify({"success": False})
    elif len(r.users) >= r.space:
        return jsonify({"success": False})
    r.users.remove(u)
    return jsonify({"success": True})

@app.route("/rooms/<int:room_id>", methods = ["GET"])
def get_room(room_id):
    r = g.session.query(Room).filter(Room.id == room_id).first()
    if r == None:
        return jsonify({"room": None})
    r = r.to_dict()
    return jsonify({"room": r})

@app.route("/users/<int:user_id>", methods = ["GET"])
def get_user(user_id):
    u = g.session.query(User).filter(User.id == user_id).first()
    if u == None:
        return jsonify({"user": None})
    user = u.to_dict()
    return jsonify({"user": user})

@app.route("/register", methods = ["PUT"])
def register():
    r = request.get_json(force=True)
    un = r.get("username")
    pw = r.get("password")

    u = g.session.query(User).filter(User.name == un).all()
    if len(u) > 0:
        return jsonify({"success": False})
    
    u = User(len(g.session.query(User).all()),un, pw)
    g.session.add(u)
    user = u.to_dict()
    return jsonify({"success": True, "user": user})

@app.route("/login", methods = ["POST"])
def login():
    r = request.get_json(force=True)
    un = r.get("username")
    pw = r.get("password")

    u = g.session.query(User).filter((User.name == un) & (User.password == pw)).all()
    if len(u) != 1:
        return jsonify({"success": False})
    user = u[0].to_dict()
    return jsonify({"success": True, "user": user})

@app.route("/connect", methods = ["POST"])
def connect():
    return jsonify({"success": True})

if __name__ == '__main__':
    inserts.setup_db()
    app.run(debug=True)