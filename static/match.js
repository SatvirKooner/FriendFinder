$(document).ready(function() {
    let socket = io.connect('https://agile-everglades-95207.herokuapp.com', { transports: ['websocket'] });
    let username = $("#matchbox").attr('data-username');

    socket.on('roomFound', function(newroom) {
        jQuery.ajax({
            type: 'POST',
            url: 'https://agile-everglades-95207.herokuapp.com/matched/' + newroom,
            async: false,
            contentType: "text/plain",  // this is the content type sent from client to server
            cache: false,
            timeout: 5000,
            success: function (data) {
                $("html").html(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                   console.log('error ' + textStatus + " " + errorThrown);
            }
        });
    });

    $('#matchbutton').on('click', function() {
        socket.emit('initiateMatch', username + ":" + socket.id);
        $('#matchbutton').css('display', 'none');
        $('#spinner').css('display', 'inline-block');
    });

});

