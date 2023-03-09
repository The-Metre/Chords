const user_name = JSON.parse(document.getElementById('user_name').textContent);

const intervals_socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/intervals/'
    + user_name
    + '/'
) 

intervals_socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('.target-note').innerHTML = (data.message);
};

intervals_socket.onclose = function(e) {
    console.error('Interval socket closed unexpectedly');
}

document.querySelector('.interval-button').onclick = function(e) {
    const current_chord = document.querySelector('.target-note');
    const message = current_chord.innerHTML;
    console.log(current_chord, message, intervals_socket)
    intervals_socket.send(JSON.stringify({
        'message': message
    }));  
}