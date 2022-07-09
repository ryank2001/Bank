/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp32-websocket-server-arduino/
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*********/

// Import required libraries
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <html.h>
#include <inlog.h>
#include "RfidDictionaryView.h"
#include <Keypad.h>

const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
  {'0','7','4','1'},
  {'0','8','5','2'},
  {'#','9','6','3'},
  {'D','C','B','A'}
};

byte colPins[COLS] = {27, 14, 12, 13}; //connect to the column pinouts of the keypad
byte rowPins[ROWS] = {26, 25, 33, 32}; //connect to the row pinouts of the keypad


//initialize an instance of class NewKeypad
Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 


const char* ssid = "Tesla IoT"; //adres van het wifinetwerk
const char* password = "fsL6HgjN";  //Wachtwoord van het wifinetwerk


enum Loginstatus { 
  scan_pas ,
  verwerken_kaartscannen , 
  kaartscan_fout, 
  geblokeerde_kaart,  
  pincode_invoeren, 
  Foute_pincode, 
  inlog_scherm, 
  saldo_zien ,
  keuzemenu_geld_opnemen,
  zelf_bedrag_kiezen,
  niet_voldoende_saldo,
  comformatie_bedrag,
  bedank_scherm,
  annulerings_scherm,
  fout_scherm,
   };

Loginstatus loginstatus = scan_pas;

gebruiker userdata;

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");


void notifyClients() {
  ws.textAll(String(1));
}



void onEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type,
             void *arg, uint8_t *data, size_t len) {
  switch (type) {
    case WS_EVT_CONNECT:
      Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
      break;
    case WS_EVT_DISCONNECT:
      Serial.printf("WebSocket client #%u disconnected\n", client->id());
      break;
    case WS_EVT_DATA:
     
      break;
    case WS_EVT_PONG:
    case WS_EVT_ERROR:
      break;
  }
}

void initWebSocket() {
  ws.onEvent(onEvent);
  server.addHandler(&ws);
}

String processor(const String& var){
  Serial.println(var);
  if(var == "STATE"){
    
      return "1";
    }
    else{
      return "1";
    
  }
  return String();
}

void scanPas(){
  
    int startBlock = 1;  // you may choose any block; choose #1 to have maximum storage availabel for the dictionary
    RfidDictionaryView rfidDict(5, 17, startBlock); // parameters: ports for SDA and RST pins, and initial block in the RFID tag

  bool tagSelected;
  ws.textAll("<h2>Welkom bij Bankoverval<br><br>Houd u pinpas tegen de scanner om te beginnen</h2>");
    
  Serial.println();
  Serial.println("Hou pinpas tegen de lezer...");

  do {
    // returns true if a Mifare tag is detected
    tagSelected = rfidDict.detectTag();
    delay(5);
  } while (!tagSelected);
  ws.textAll("<h2>kaart gedetecteerd</h2>");
  Serial.println(" Pinpas gedetecteerd");
  loginstatus = verwerken_kaartscannen;
}

void verwerkenKaartscannen(){
  ws.textAll("<h2>kaart gedetecteerd <br> informatie wordt verwerkt</h2>");
  if (!userdata.set_name("johan")){
    loginstatus = kaartscan_fout;
    return;
  }
  if (!userdata.set_iban("NL00RABO54362346")){
    loginstatus = kaartscan_fout;
    return;
  }
  userdata.seetpincodepogingen(3);
  userdata.set_saldo();
  loginstatus = pincode_invoeren;
  delay(1000);
}

void KaartscanFout(){
  ws.textAll("<h2>Fout bij scannen van kaart, transactie wordt afgebroken</h2>");
  userdata.clearuser();
  loginstatus = scan_pas;
  delay(4000);
}

void pincodeInvoeren(){
  String pincodet = "<h2>Voer u 4 cijverige pincode in <br></h2>";
  String getalt = "";
  String endt = "</h2>";
  ws.textAll(pincodet + getalt + endt);
  while (true){
      char customKey = customKeypad.getKey();
      if (customKey){
        Serial.print("alive");
        if (customKey == 'D'){
          loginstatus = scan_pas; //moet naar annullerings scherm!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          break;
        }
        else {
          userdata.add_number_pincode(customKey);
          getalt.concat("*") ;
          ws.textAll(pincodet + getalt + endt);
        }
      }
      if (userdata.getPincode().length() == 4){
        if (userdata.checkpin()){
          loginstatus = inlog_scherm;
          break;
        }
        else{
          loginstatus = Foute_pincode;
          break;
        }
      }
  
  }
}

void foutePincode(){
  userdata.reducePogingen();
  if(userdata.getPogingen() == 0){
     ws.textAll("<h2>uw pas is geblokeerd<h2>");
     delay(5000);
     userdata.clearpin();
     loginstatus = scan_pas;
     return;
  }
  String een = "<h2>Foute pincode ingevoert, probeer het op nieuw <br> U heeft nog ";
  String twee = " pogingen</h2>";
  ws.textAll(een + userdata.getPogingen() + twee);
  userdata.clearpin();
  delay(3000);
  
  loginstatus = pincode_invoeren;

  
}

void inlogscherm(){
  //ik heb eerste haakje verandert naar single ipv dubbel!!!!!
  ws.textAll(R"rawliteral(     
        <div class="input panel"></div>
        <div class="text panel"></div>
        <div class="options en text panel">
            <div class="option-vraag"> Welkom Leon, kies een optie</div>
            <div class="option-container">
                <!--er passen max 7 op huidige blok afmetingen!!-->
                <div class="option"> 
                    <p class="option-text">Bekijk uw saldo </p>
                    <div class="option-toets">1</div>
                </div>
                <div class="option"> 
                    <p class="option-text">Geld opnemen</p>
                    <div class="option-toets">2</div>
                </div>
                <div class="option"> 
                    <p class="option-text">Transactie afbreken</p>
                    <div class="option-toets">D</div>
                </div>

            <!-- <div class="cancel-butt">cancel/terug</div>
            <div class="help-butt">help</div> -->
            </div>
        </div>)rawliteral");
  while (true){
      char customKey = customKeypad.getKey();
      if (customKey){
        if (customKey== '1'){
          loginstatus = saldo_zien;
          break;
        }
        if (customKey== '2'){
          loginstatus = keuzemenu_geld_opnemen;
          break;
        }
        if (customKey== 'D'){
          loginstatus = annulerings_scherm;
          break;
        }
      }
  }
}

void saldoZien(){
ws.textAll(R"rawliteral(    <div class="input panel"></div>
        <div class="text panel"></div>
        <div class="options en text panel">
            <div class="option-vraag"> Welkom Leon, Uw saldo is 100 euro</div>
            <div class="option-container">
                <!--er passen max 7 op huidige blok afmetingen!!-->
                <div class="option"> 
                    <p class="option-text">Geld opnemen </p>
                    <div class="option-toets"> 2</div>
                </div>
                <div class="option"> 
                    <p class="option-text">Transactie afbreken</p>
                    <div class="option-toets">D</div>
                </div>

            <!-- <div class="cancel-butt">cancel/terug</div>
            <div class="help-butt">help</div> -->
            </div> 
          </div>)rawliteral");
while (true){
      char customKey = customKeypad.getKey();
      if (customKey){
        if (customKey== '2'){
          loginstatus = keuzemenu_geld_opnemen;
          break;
        }
        if (customKey== 'D'){
          loginstatus = annulerings_scherm;
          break;
        }
      }
  }
}

void keuzemenuGeldOpnemen(){
ws.textAll(R"rawliteral(  <div class="options en text panel">
          <div class="option-vraag">Kies het bedrag dat u wilt opnemen</div>
          <div class="options-grid">
              <!--er passen max 6 op huidige blok afmetingen!! met option!! class-->
              <div class="option2"> 
                  <p class="option2-text">10 Euro</p>
                  <div class="option2-toets">1</div>
              </div>
              <div class="option2"> 
                <p class="option2-text">20 Euro</p>
                <div class="option2-toets"> 2</div>
              </div>
              <div class="option2"> 
                <p class="option2-text">50 Euro</p>
                <div class="option2-toets"> 3</div>
              </div>
              <div class="option2"> 
                <p class="option2-text">100 Euro</p>
                <div class="option2-toets"> 4</div>
              </div>
              <div class="option2"> 
                <p class="option2-text">150 Euro</p>
                <div class="option2-toets"> 5</div>
              </div>
              <div class="option2"> 
                <p class="option2-text">Ander bedrag</p>
                <div class="option2-toets"> 6</div>
              </div>
              <div class="option2"> 
                <p class="option2-text">Stop transactie</p>
                <div class="option2-toets"> D</div>
              </div>
          <!-- <div class="cancel-butt">cancel/terug</div>
          <div class="help-butt">help</div> -->
          </div>
      </div>)rawliteral");
while (true){
      char customKey = customKeypad.getKey();
      if (customKey){
        if (customKey== '1'){
          if(userdata.set_opnamehoeveelheid(10)){
            loginstatus = comformatie_bedrag;
          break;
          }
          else{
            loginstatus = niet_voldoende_saldo;
            break;
          }
        }
        if (customKey== '2'){
          if(userdata.set_opnamehoeveelheid(20)){
            loginstatus = comformatie_bedrag;
          break;
          }
          else{
            loginstatus = niet_voldoende_saldo;
            break;
          }
        }
        if (customKey== '3'){
          if(userdata.set_opnamehoeveelheid(50)){
            loginstatus = comformatie_bedrag;
          break;
          }
          else{
            loginstatus = niet_voldoende_saldo;
            break;
          }
        }
        if (customKey== '4'){
          if(userdata.set_opnamehoeveelheid(100)){
            loginstatus = comformatie_bedrag;
          break;
          }
          else{
            loginstatus = niet_voldoende_saldo;
            break;
          }
        }
        if (customKey== '5'){
          if(userdata.set_opnamehoeveelheid(150)){
            loginstatus = comformatie_bedrag;
          break;
          }
          else{
            loginstatus = niet_voldoende_saldo;
            break;
          }
        }
        if (customKey== '6'){
          loginstatus = zelf_bedrag_kiezen;
          break;
        }
        if (customKey== 'D'){
          loginstatus = annulerings_scherm;
          break;
        }
      }
  }
}

void zelfBedragKiezen(){
  ws.textAll(R"rawliteral(         
   <div class="options en text panel">
          <div class="option-vraag3">Voer zelf een hoeveelheid in om opgenomen te worden<br> Minimaal 10 euro en maximaal 300 euro<br><br>_ _ _</br></div>
                 <div class="option-container">
                     <!--er passen max 7 op huidige blok afmetingen!!-->
                     <div class="option"> 
                         <p class="option-text">Bevestig bedrag</p>
                         <div class="option-toets">#</div>
                     </div>
                     <div class="option"> 
                       <p class="option-text">Stop transactie</p>
                       <div class="option-toets"> 1</div>
                     </div>
                </div>   
     
                 <!-- <div class="cancel-butt">cancel/terug</div>
                 <div class="help-butt">help</div> -->
             </div>
         </div>)rawliteral");
  String hoeveelheid = "";
  while (true){
      char customKey = customKeypad.getKey();
      if (customKey){
        
        if (customKey == 'D'){
          loginstatus = annulerings_scherm;
          break;
        }
        else if (customKey == '#'){
          if(userdata.set_opnamehoeveelheid(hoeveelheid.toInt())){
            loginstatus = comformatie_bedrag;
          break;
          }
          else{
            loginstatus = niet_voldoende_saldo;
            break;
          }
        }
        else if (customKey == 'A'||customKey == 'B'||customKey == 'C'){
        }
        else {
          hoeveelheid.concat(customKey);
        }
      }
      
  }
}

void nietVoldoendeSaldo(){
    ws.textAll(R"rawliteral( <div class="options en text panel">
          <div class="option-vraag4">U heeft niet voldoende saldo voor deze transactie</div>
          <div class="option-container">
              <!--er passen max 7 op huidige blok afmetingen!!-->
              <div class="option"> 
                  <p class="option-text">Bekijk uw saldo</p>
                  <div class="option-toets">1</div>
              </div>
              <div class="option"> 
                <p class="option-text">Neem een ander bedrag op</p>
                <div class="option-toets"> 2</div>
              </div>
              <div class="option"> 
                <p class="option-text">Stop transactie</p>
                <div class="option-toets"> D</div>
              </div>
          <!-- <div class="cancel-butt">cancel/terug</div>
          <div class="help-butt">help</div> -->
          </div>
      </div>)rawliteral");
  while (true){
      char customKey = customKeypad.getKey();
      if (customKey){
        if (customKey== '1'){
          loginstatus = saldo_zien;
          break;
        }
        if (customKey== '2'){
          loginstatus = keuzemenu_geld_opnemen;
          break;
        }
        if (customKey== 'D'){
          loginstatus = annulerings_scherm;
          break;
        }
      }
  }
}

void comformatiescherm(){
  String string1 = R"rawliteral(<h2>U staat op het punt )rawliteral";
  String string2 = R"rawliteral( euro op te nemen</div>
          <div class="option-container">
              <!--er passen max 7 op huidige blok afmetingen!!-->
              <div class="option"> 
                  <p class="option-text">Neem dit bedrag op</p>
                  <div class="option-toets">1</div>
              </div>
              <div class="option"> 
                <p class="option-text">Neem een ander bedrag op</p>
                <div class="option-toets"> 2</div>
              </div>
              <div class="option"> 
                <p class="option-text">Stop transactie</p>
                <div class="option-toets"> D</div>
              </div>
          <!-- <div class="cancel-butt">cancel/terug</div>
          <div class="help-butt">help</div> -->
          </div>
      </div>)rawliteral";
  ws.textAll(string1 + userdata.getopname() + string2);
 while (true){
      char customKey = customKeypad.getKey();
      if (customKey){
        if (customKey== '1'){
          loginstatus = bedank_scherm;
          break;
        }
        if (customKey== '2'){
          loginstatus = keuzemenu_geld_opnemen;
          break;
        }
        if (customKey== 'D'){
          loginstatus = annulerings_scherm;
          break;
        }
      }
  }
}

void bedankScherm(){
  ws.textAll("<h2>Dankuwel voor pinnen bij de bankoverval <br> Het geld en bon worden nu uitgegeven</h2>");
  userdata.opnemenBedrag();
  userdata.clearuser();
  delay(9000);
  loginstatus = scan_pas;
}

void annuleringsScherm(){
  ws.textAll("<h2>Transactie geannuleerd</h2>");
  userdata.clearuser();
  delay(9000);
  loginstatus = scan_pas;
}

void setup(){
  // Serial port for debugging purposes
  Serial.begin(115200);

  
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  // Print ESP Local IP Address
  Serial.println(WiFi.localIP());

  initWebSocket();

  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", index_html, processor);
  });

  // Start server
  server.begin();
}

void loop() {
  ws.cleanupClients();
  switch (loginstatus)
  {
  case scan_pas:
    scanPas();
    break;
  case verwerken_kaartscannen:
    verwerkenKaartscannen();
    break;
  case kaartscan_fout:
    KaartscanFout();
    break;
  case geblokeerde_kaart:
    break;
  case pincode_invoeren:
    pincodeInvoeren();
    break;
  case Foute_pincode:
    foutePincode();
    break; 
  case inlog_scherm:
    inlogscherm();
    break; 
  case saldo_zien:
    saldoZien();
    break; 
  case keuzemenu_geld_opnemen:
    keuzemenuGeldOpnemen();
    break; 
  case zelf_bedrag_kiezen:
    zelfBedragKiezen();
    break;
  case niet_voldoende_saldo:
    nietVoldoendeSaldo();
    break;
  case comformatie_bedrag:
    comformatiescherm();
    break; 
  case bedank_scherm:
    bedankScherm();
    break; 
  case annulerings_scherm:
    annuleringsScherm();
    break;  
  case fout_scherm:

    break; 
  default:
    break;
  }

}