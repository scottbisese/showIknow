function disableButton() {
    var x = document.getElementById("button1");
    x.disabled = true;
}

function showDatetime() {
    var x = document.getElementById("datetime");
    x.innerHTML = Date();
}

function colorChanger() {
    var x = document.getElementById("button3");
    x.style.color = '#'+(0x1000000+Math.random()*0xffffff).toString(16).substr(1,6);
}

function biggerFont() {
    var x = document.getElementById("button4");
    x.style.fontSize = parseInt(x.style.fontSize.replace("px", "")) + 10 + "px";
}

function refreshPage() {
    location.reload();
}

function redirect() {
    location.href = "https://www.drake.edu/";
}

function alertButton() {
    window.alert("This is an alert! You have been warned!");
}

function createButton() {
  var x = document.createElement("BUTTON");
  var t = document.createTextNode("Useless Button");
  x.appendChild(t);
  document.body.appendChild(x);
}