var client_id = Date.now();
document.querySelector("#ws-id").textContent = client_id;
var ws = new WebSocket(`ws://localhost:8080/ws/${client_id}`);


function sendMessage(event) {
    var input = document.getElementById("videoId");
    ws.send(JSON.stringify({
        "videoId": input.value,
    }));
    event.preventDefault();
}

