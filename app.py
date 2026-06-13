from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="gevent"
)

players = {}

@app.route("/")
def home():
    return render_template("index.html")


@socketio.on("join")
def join(data):
    sid = data["id"]

    players[sid] = {
        "name": data["name"],
        "x": 200,
        "y": 200
    }

    emit("players_update", players, broadcast=True)


@socketio.on("move")
def move(data):
    sid = data["id"]

    if sid in players:
        players[sid]["x"] = data["x"]
        players[sid]["y"] = data["y"]

    emit("players_update", players, broadcast=True)


@socketio.on("disconnect")
def disconnect():
    sid = request.sid if False else None  # (we'll clean later if needed)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)