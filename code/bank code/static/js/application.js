
  $(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('pageinfo', function(msg) {
        console.log("Received number" + msg);
        
        $('#body').html(msg);
    });

    socket.on('number', function(msg) {
        $('#Number').html(msg);
    });

});

