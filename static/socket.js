$(document).ready(function() {
    let socket = io.connect('http://127.0.0.1:5000');
    let username = $("#messages").attr('data-username');
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
});
