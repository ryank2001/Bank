
const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
    <title>ESP Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <!-- <link rel="stylesheet" href="styleVoorACM.css"> -->
  <title>ESP Web Server</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">
  <style>








.option-vraag{
    align-content: center;
    font-size: 40px;
    /*line-height: 10px; /*bij 2+zinnen dit weg halen?*/
    color: #000000;
    height: 50px;
    width: 700px;
    top: 0 ;
    display: inline-block;
    vertical-align: middle;
}

.option-vraag4{
    align-content: center;
    font-size: 30px;
    /*line-height: 10px; /*bij 2+zinnen dit weg halen?*/
    color: #000000;
    height: 50px;
    width: 700px;
    top: 0 ;
    display: inline-block;
    vertical-align: middle;
}


.cancel-butt{
    left: 0;
    bottom: 0;
    height: 46px;
    line-height: 50px;
    width: 90px;
    background-color: #51536349;
    position: absolute;

    border: 2px solid rgb(0, 0, 0);
    border-radius: 5px;
    
}
.help-butt{
    right: 0;
    bottom: 0;
    height: 46px;
    line-height: 50px;
    width: 90px;
    background-color: #51536349;
    position: absolute;
    border: 2px solid rgb(0, 0, 0);
    border-radius: 5px;
}

.option{
    position: relative;     
    /* WIDHT IS KLEINER DAN 500 DOOR BORDER!! */
    width: 800px; 
    height: 60px;
    background-color: #a7a7a7;
    border: 2px solid rgb(0, 0, 0);
    border-radius: 5px;
    margin-bottom: 5px;
}
.option-text{
    position: absolute; 
    left: 5px;
    bottom: -6.5px;
    font-size: 30px;
    /* height: 30px;
    line-height: 30px;
    align-content: center; */
}

.option-toets{
    position: absolute; 
    right: 2px;
    top: 3px;
    height: 45px;
    width: 45px;
    background-color: #ffffff;
    border: 2px solid rgb(0, 0, 0);

    align-content: center;
    font-size: 30px;
    color: #000000;
}

.options-grid{
  display: grid;
  row-gap: 5px;
  grid-template-columns: auto auto;
  padding: 5px;

  width: 756px;
  height: 300px;
  align-content: center;
    
}
.option2-toets{
  position: absolute; 
  right: 2px;
  top: 3px;
  height: 30px;
  width: 30px;
  background-color: #ffffff;
  border: 2px solid rgb(0, 0, 0);

  align-content: center;
  font-size: 25px;
  color: #000000;
}
.option2-text{
  position: absolute; 
  left: 5px;
  bottom: -6.5px;
  font-size: 25px;
}
.option2{
  position: relative;     
  /* WIDHT IS KLEINER DAN 500 DOOR BORDER!! */
  width: 345px; 
  height: 50px;
  background-color: #a7a7a7;
  border: 2px solid rgb(0, 0, 0);
  border-radius: 5px;
  margin-bottom: 5px;
}
.option-vraag3{
  align-content: center;
  font-size: 30px;
  /*line-height: 10px; /*bij 2+zinnen dit weg halen?*/
  color: #000000;
  height: 188px;
  width: 700px;
  top: 0 ;
  display: inline-block;
  vertical-align: middle;

}

/*-=-=-=-=-=-==-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==*/

html {
    font-family: Arial, Helvetica, sans-serif;
    text-align: center;
  }
  h1 {
    font-size: 25px;
    color: white;
  }
  h2{
    font-size: 25px;
    font-weight: bold;
    color: #143642;
  }
  .topnav {
    overflow: hidden;
    background-color: #143642;
  }
  body {
    margin: 0;
  }
  .content {
    max-width: 806px;
    margin: 0 auto;
  }
  .button {
    padding: 15px 50px;
    font-size: 24px;
    text-align: center;
    outline: none;
    color: #fff;
    background-color: #0f8b8d;
    border: none;
    border-radius: 5px;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    -webkit-tap-highlight-color: rgba(0,0,0,0);
   }
   /*.button:hover {background-color: #0f8b8d}*/
   .button:active {
     background-color: #0f8b8d;
     box-shadow: 2 2px #CDCDCD;
     transform: translateY(2px);
   }
   .state {
     font-size: 1.5rem;
     color:#8c8c8c;
     font-weight: bold;
   }


  </style>

  </head>
  <body>
    </div>
    <div class="content" >
    <!-- Hier staat card panel info content -->
      <div class="card-container" id="demo">
       
        <h2>Welkom bij Bankoverval<br><br>Houd u pinpas tegen de scanner om te beginnen.</h2>

      </div>
    </div>



  <script>
    var gateway = `ws://${window.location.hostname}/ws`;
    var websocket;
    window.addEventListener('load', onLoad);
    function initWebSocket() {
      console.log('Trying to open a WebSocket connection...');
      websocket = new WebSocket(gateway);
      websocket.onopen    = onOpen;
      websocket.onclose   = onClose;
      websocket.onmessage = onMessage; // <-- add this line
    }
    function onOpen(event) {
      console.log('Connection opened');
    }
    function onClose(event) {
      console.log('Connection closed');
      setTimeout(initWebSocket, 2000);
    }
    function onMessage(event) {
      var state;
      document.getElementById("demo").innerHTML = event.data;
     
    }
    function onLoad(event) {
      initWebSocket();
    
    }
  
  </script>
  </body>
  </html>
)rawliteral";