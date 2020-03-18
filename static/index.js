//Load user name
document.addEventListener('DOMContentLoaded', ()=>{

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
  document.querySelector('#username').innerHTML= localStorage.getItem('user');

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
          msg_div.innerHTML = item.user +": " + item.msg

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


})
