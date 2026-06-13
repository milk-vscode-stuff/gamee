from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

players = {}
walls = []

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("join")
def join(data):
    sid = request.sid
    players[sid] = {"name": data.get("name", "Player"), "x": 200, "y": 200}
    emit("players_update", players, broadcast=True)
    emit("walls_update", walls, broadcast=True)

@socketio.on("move")
def move(data):
    sid = request.sid
    if sid in players:
        players[sid]["x"] = data.get("x", 0)
        players[sid]["y"] = data.get("y", 0)
    emit("players_update", players, broadcast=True)

@socketio.on("place_wall")
def place_wall(data):
    walls.append({
        "x": data["x"],
        "y": data["y"],
        "w": data.get("w", 80),
        "h": data.get("h", 20)
    })
    emit("walls_update", walls, broadcast=True)

@socketio.on("clear_walls")          # ← NEW
def clear_walls():
    walls.clear()
    emit("walls_update", walls, broadcast=True)

@socketio.on("disconnect")
def disconnect():
    sid = request.sid
    if sid in players:
        del players[sid]
    emit("players_update", players, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)