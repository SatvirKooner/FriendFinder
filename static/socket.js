$(document).ready(function() {
    let socket = io.connect('http://127.0.0.1:5000');
    let username = $("#messages").attr('data-username');
    let video = document.querySelector("#myStream");
    let canvas = document.querySelector("#canvas");
    let ctx = canvas.getContext("2d");
    let localMediaStream = null;
    let streamInterval;
    
    socket.on('connect', function() {
        socket.emit('init',  username );
    });

    socket.on('init', function(loginUser) {
        $("#messages").append('<li>' + loginUser + " has connected to the server!" +'</li>');
    });

    socket.on('publicMessage', function(payload) {
        $("#messages").append('<li>' + '[' + payload.msgFrom + ']' + ': ' + payload.msg+'</li>');
    });

    $('#sendbutton').on('click', function() {
        payload = {'msg':$('#myMessage').val(), 'msgFrom' : username}
        socket.emit('publicMessage', payload);
        $('#myMessage').val('');
    });

    function sendFrame() {
        if(!localMediaStream){
            return;
        }
        ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0 , 300, 150);
        
        let dataURL = canvas.toDataURL('image/jpeg');
        socket.emit('input_frame', dataURL);
    }

    let constraints = {
        video: {
            width: { min: 400 },
            height: { min: 480 }
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
