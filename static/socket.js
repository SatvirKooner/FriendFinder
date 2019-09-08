$(document).ready(function() {
    let socket = io.connect('https://agile-everglades-95207.herokuapp.com', { transports: ['websocket'] });
    let username = $("#messages").attr('data-username');
    let streamID = $("#messages").attr('data-streamID');
    let room = $("#messages").attr('data-room');
    let video = document.querySelector("#myStream");
    let canvas = document.querySelector("#canvas");
    let ctx = canvas.getContext("2d");
    let localMediaStream = null;
    let streamInterval;
    
    socket.on('connect', function() {
        payload = {
            username,
            room
        }
        socket.emit('init',  payload);
        console.log(payload);
    });

    socket.on('init', function(loginUser) {
        $("#messages").append('<li>' + loginUser + " has connected to the server!" +'</li>');
    });

    socket.on('publicMessage', function(payload) {
        $("#messages").append('<li>' + '[' + payload.msgFrom + ']' + ': ' + payload.msg+'</li>');
    });

    $('#sendbutton').on('click', sendMessage);
    $('#myMessage').keypress(event => {if (event.which == 13) sendMessage()});

    function sendMessage() {
        let msg = $('#myMessage').val();
        if (!msg)
            return;
        payload = {msg, 'msgFrom' : username, room}
        socket.emit('publicMessage', payload);
        $('#myMessage').val('');
    }

    function sendFrame() {
        if(!localMediaStream){
            return;
        }
        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0 , 300, 150);
        
        let dataURL = canvas.toDataURL('image/jpeg');
        payload = {
            dataURL,
            streamID
        }
        socket.emit('input_frame', payload);
    }

    let constraints = {
        video: {
            width: { min: 400 },
            height: { min: 300 }
        }
    };

    $("#uploadbutton").on('click', function(){
        if(streamInterval)
            return
        navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
            video.srcObject = stream;
            localMediaStream = stream;

            streamInterval = setInterval(function() {
                sendFrame();
            }, 25);
        }).catch(function(error) {
            console.log(error);
        })
    });

    $("#stopbutton").on('click', () => {
        clearInterval(streamInterval);
        streamInterval=null;
    });
});
