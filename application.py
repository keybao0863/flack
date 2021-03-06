import os
import json
from datetime import datetime
from flask import Flask, render_template, request, flash, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)

channels = []
channels.append("default")
map = {}
msg_test = [];

map["default"] = msg_test;

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

@app.route("/getmessages", methods=["POST"])
def getmessages():

    #Find which channel is requesting
    channel = request.form["channel"]

    #Make sure channel exists
    if(channel not in channels):
        return jsonify({"fail":"true"})

    #Get the message from the channel and return
    messages = map[channel]

    #Change current channel
    global current_channel
    current_channel = channel

    return json.dumps(messages)

@socketio.on('send message')
def send(data):

    #Retrieve message
    user = data["user"];
    message = data["message"]

    #Get current time
    dt = datetime.now()
    time = dt.strftime("%m/%d/%y %I:%M%p ")

    #Add to current message list
    map[current_channel].append({"user":user, "msg":message, "time":time});

    # Make sure message list is not over 100
    if(len(map[current_channel]) > 100):
        map[current_channel] = map[current_channel][-100:]

    #Broadcast message
    emit("announce message", {"user":user, "message":message, "time":time}, broadcast = True)
