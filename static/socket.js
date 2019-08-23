$(document).ready(function() {
    let socket = io.connect('http://127.0.0.1:5000');
    let username = $("#messages").attr('data-username');
    socket.on('connect', function() {
        socket.send(username +' has connected!');
    });
    socket.on('message', function(msg) {
        if(msg.indexOf('has connected'))
        $("#messages").append('<li>' + '[' + username + ']' + ': ' + msg+'</li>');
    });
    $('#sendbutton').on('click', function() {
        socket.send($('#myMessage').val());
        $('#myMessage').val('');
    });
});
