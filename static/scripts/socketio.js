document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    let room = "Lounge";
    joinRoom("Lounge");

    //Sending message on connect
    socket.on('connect', () => {
        socket.send({'msg': "Has joined",'username': username});
    });
    // Receiving message
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        if(data.username){
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
        }
        else{
            printSysMsg(data.msg);
        }
    });
    // Sending message on send
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value, 'username': username, 'room': room});
        //Clear input area
        document.querySelector('#user_message').value = '';
    }
    // Room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.addEventListener('click', () => {
            let newRoom = p.innerHTML;
            if(newRoom == room){
                msg = `You are already in the ${room} room.`;
                printSysMsg(msg);
            }
            else{
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        });
    });
    //Leave room
    function leaveRoom(room){
        socket.emit('leave', {'username': username, 'room': room});
    }
    //Join room
    function joinRoom(room){
        socket.emit('join', {'username': username, 'room': room});
        //Clear message area
        document.querySelector('#display-message-section').innerHTML = '';
    }
    //Print system message
    function printSysMsg(msg){
        const p = document.createElement('p')
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
});