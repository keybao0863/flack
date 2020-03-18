//Load user name
document.addEventListener('DOMContentLoaded', ()=>{
  ///Configure Websocket

  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  //When connected, configure send button
  socket.on('connect', () => {
    document.querySelector("#send-button").onclick = () =>{

      //Get the message
      const user = localStorage.getItem('user')
      const msg = document.querySelector("#send").value

      //Emit message
      socket.emit('send message', {'user':user, 'message':msg})

      //Clear input box
      document.querySelector("#send").value=""
    }
  })

  //When message is annouced, add to message list
  socket.on('announce message', data =>{

    //Create Element to hold message
    let msg_div = document.createElement("div")
    msg_div.innerHTML = data.time + " " + data.user +": " + data.message

    // Append to message box
    document.querySelector("#message-box").appendChild(msg_div)
  })



  //If first time user, prompt for a user name
  if(!localStorage.getItem('user')){

    console.log("no user")
    var username = prompt("Please enter a username to display:");
    localStorage.setItem('user', username);
  }
  else{
    console.log("user exists")
    console.log(localStorage.getItem('user'))
  }

  //Display username in the message box
  document.querySelector('#username').innerHTML= "You are logged in as: " + localStorage.getItem('user');

  //Once a channel is clicked, load its messages
  document.querySelectorAll('.channels').forEach(channel => {
    channel.onclick = () => {
      // Submit a POST request to server to obtain messages associated with channel
      const channel_name = channel.innerHTML;
      const request = new XMLHttpRequest();
      request.open('POST', '/getmessages')

      // Callback function for when request if complete
      request.onload = () => {

        // Extract messages from response
        const data = JSON.parse(request.responseText);

        //Clear old messages
        const box = document.querySelector("#message-box")
        while (box.hasChildNodes()) {
          box.removeChild(box.childNodes[0]);
        }

        //For each message, create a div to show in message box
        data.forEach(item => {

          //Creat element
          let msg_div = document.createElement("div")
          msg_div.innerHTML = item.time +" " +item.user +": " + item.msg

          // Append to message box
          document.querySelector("#message-box").appendChild(msg_div)
        });


      }

      //Send the data
      const data = new FormData();
      data.append('channel', channel_name);
      request.send(data);
      return false;

    }

  });

  //Allow send button to be pushed with Enter key
  // Execute a function when the user releases a key on the keyboard
  document.addEventListener("keyup", function(event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      document.querySelector("#send-button").click();
    }
  });
})
