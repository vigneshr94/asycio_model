var client_id = Date.now();
document.querySelector("#ws-id").textContent = client_id;
var ws = new WebSocket(`ws://localhost:8080/ws/${client_id}`);

ws.onmessage = function (event) {
    console.log(event.data);
    var messages = document.getElementById("messages");
    var message = document.createElement("li");
    var content = document.createTextNode(event.data);
    message.appendChild(content);
    messages.appendChild(message);
};

function sendMessage(event) {
    var input = document.getElementById("videoId");
    ws.send(input.value);
    input.value = "";
    event.preventDefault();
}

