# pip install flask-socketio

from flask import Flask, send_from_directory
from flask_socketio import SocketIO, send

app=Flask(__name__)
app.config["SECRET_KEY"] = "my-secret-key"
socketIO = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory("static","index.html")

@socketIO.on("message")
def handle_message(msg):
    print("Message:", msg)
    send (msg, broadcast=True)

if __name__ =="__main__":

    # app.run(debug=True)
    socketIO.run(app,debug=True)