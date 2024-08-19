from flask import Flask, send_file, jsonify, request  # Import request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app) 

status = "Stopped"

# Static files in clips
@app.route("/files/clip/<path:path>")
def serve_clip(path):
    return send_file(os.path.join("clips", path))


@app.route("/files/imgs/<path:path>")
def serve_static(path):
    return send_file(os.path.join("imgs", path))


@app.route("/files/takes/<path:path>")
def serve_takes(path):
    return send_file(os.path.join("takes", path))


@app.route("/")
def serve_client():
    return send_file("client.html")


@app.route("/socket.io.js")
def serve_socketio():
    return send_file("socket.io.js")


@app.route("/server")
def serve_server():
    return send_file("server.html")


@app.route("/files/clips")
def list_clips():
    # Ensure the clips directory exists to avoid errors
    if not os.path.exists("clips"):
        return jsonify([])  # Return an empty list if the directory does not exist
    clips = os.listdir("clips")
    clips = [clip for clip in clips if clip.endswith(".mp4")]
    return jsonify(clips)


@socketio.on("connect")
def handle_connect():
    print(f"a user connected, id: {request.sid}")
    emit("status", status)


@socketio.on("disconnect")
def handle_disconnect():
    print(f"user disconnected, id: {request.sid}")


@socketio.on("status")
def handle_status_update(data):
    print(f"status update: {data}")
    global status
    status = data
    emit("status", data, broadcast=True)


if __name__ == "__main__":
    print("Server running on http://localhost:3000")
    socketio.run(app, host="0.0.0.0", port=3000)
