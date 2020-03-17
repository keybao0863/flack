//Load user name
window.addEventListener('DOMContentLoaded', ()=>{

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

  document.querySelector('#username').innerHTML= localStorage.getItem('user');
})
