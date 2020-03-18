import os
import json
from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)

channels = []
channels.append("test channel")
map = {}
current_channel = "test channel"

# Generate some fake messages for testing
msg_test = [];
map["test channel"] = msg_test;
msg_test.append({
    "user" : "keybao",
    "msg" : "hello 1",
    "time":"2020/03/18 9:55:00"
})

msg_test.append({
    "user" : "keybao2",
    "msg" : "hello2",
    "time":"2020/03/18 9:55:00"
})



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

    #Genera Testing msgs
    messages.append({"user":"keybao3", "msg":"test3", "time":"2020/03/18 9:55:00"})
    #
    flash("Channel created")
    return render_template("index.html", channels = channels)

@app.route("/getmessages", methods=["POST"])
def getmessages():

    #Find which channel is requesting
    channel = request.form["channel"]

    #Make sure channel exists
    if(channel not in channels):
        return render_template("error.html", message = "Channel does not exist.")

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
    time = dt.strftime("%d. %B %Y %I:%M%p ")

    #Add to current message list
    # TODO: Make sure message list is not over 100
    map[current_channel].append({"user":user, "msg":message, "time":time});

    #Broadcast message
    emit("announce message", {"user":user, "message":message, "time":time}, broadcast = True)
