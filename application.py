import os

from flask import Flask, render_template, request, flash
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)

channels = []
channels.append("test channel")
map = {}

@app.route("/")
def index():
    return render_template('index.html', channels = channels)

@app.route("/newchannel", methods=["POST"])
def new_channel():

    #Make sure channel does not exist
    input = request.form['name']
    if(input in channels):
        return render_template("error.html", message="This channel already exists")

    #Create new channel
    messages = []
    map[input] = messages
    channels.append(input)
    flash("Channel created")
    return render_template("index.html", channels = channels)
