
import codecs
from flask import Flask, render_template
from time import sleep
from threading import Thread, Event
from cardreader import CardReader
from Numpad import Numpad
from enum import Enum
from geldsysteem import moneydispenser
from bonprinter import bonprinter
from flask_socketio import SocketIO, emit
from Numpad import Numpad
from WebSocket import *
from userdata import *



__author__ = 'Ryan'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)
bon = bonprinter()
thread = Thread()
thread_stop_event = Event()
numpad = Numpad()
userdata = UserData()
reader = CardReader()
geld = moneydispenser()


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


class LoginStatus(Enum):
    scan_pas =1
    verwerken_kaartscannen =2
    kaartscan_fout =3
    geblokeerde_kaart =4
    pincode_invoeren =5
    Foute_pincode =6
    inlog_scherm =7
    saldo_zien =8
    brief_keuze = 9
    zelf_bedrag_kiezen =10
    niet_voldoende_saldo =11
    comformatie_bedrag  =12
    bedank_scherm =13
    annulerings_scherm =14
    fout_scherm= 15
    bon_keuze = 16
   




def scanPas() -> LoginStatus:
    """
    Functie voor het weergeven van het kaart scan scherm.
    Deze functie bijft scannen voor een kaart en zodra deze er een gevonden heeft zal deze naar het kaart verwerk scherm gaan.

    returns LoginStatus.scan_pas om terug te gaan naar het kaartscan scherm.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Start.html", "r", "utf-8").read(), namespace='/test')
    reader.checkcard()
    return LoginStatus.verwerken_kaartscannen

def verwerkenKaart()-> LoginStatus:
    """
    Functie voor het weergeven van het verwerken kaart scherm.
    Daarnaast laad deze functie de data van de kaart in en checked of deze klopt.

    returns LoginStatus.scan_pas om terug te gaan naar het kaartscan scherm.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Informatie_wordt_verwerkt.html", "r", "utf-8").read(), namespace='/test')
    iban = reader.getiban()
    status = userdata.setIban(iban)
    sleep(1)
    if status == 0:
        return LoginStatus.kaartscan_fout
    pogingen = userdata.getpincodepogingen()
    if isinstance(pogingen,str):
        return LoginStatus.kaartscan_fout
    elif pogingen == 0:
        return LoginStatus.geblokeerde_kaart
    else:
        return LoginStatus.pincode_invoeren
        
    

def geblokeerdeKaart()-> LoginStatus:
    """
    Functie voor het weergeven van het geblokeerde kaart scherm.
    Daarnaast leegt deze functie alle data van de huidige transactie.

    returns LoginStatus.scan_pas om terug te gaan naar het kaartscan scherm.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Pas blocked.html", "r", "utf-8").read(), namespace='/test')
    sleep(5)
    userdata.clearUserData()
    return LoginStatus.scan_pas

def pincodeInvoer()-> LoginStatus:
    """
    Functie voor het weergeven van het pincode invoer scherm.
    In dit scherm kan de gebruiker zijn pincode invoeren of transactie afbreken.
    door te kiezen uit een van deze opties:
    0-9: Getal aan pincode toevoegen
    C: Getal weghalen
    D: Transactie afbreken

    returns een LoginStatus op basis van de door de gebruiker gemaakte keus.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Pincode invoeren.html", "r", "utf-8").read(), namespace='/test')
    while True:
        char = numpad.getInput()
        if char == "D":
            return LoginStatus.annulerings_scherm
        elif char ==  "C":
            userdata.removePincodeNumber()
            socketio.emit('number', userdata.getpincode(), namespace='/test')
        elif char == "A" or char =="B" or char =="C" or char=="#" or char == "*":
            pass
        else:
            userdata.addPincodeNumber(char)
            socketio.emit('number', userdata.getpincode(), namespace='/test')
            if userdata.checkPinSize() == 1:
                print(userdata.getpincode())
                
                var = userdata.checkpincode()
                
                if var == 1:
                    return LoginStatus.inlog_scherm
                elif var == "something went wrong":
                    return LoginStatus.fout_scherm
                else:
                    return LoginStatus.Foute_pincode
       
        sleep(0.3)


def foutePincode()-> LoginStatus:
    """
    Functie voor het weergeven van het foute pincode scherm.
    Dit scherm update het aantal pogingen die de gebruiker nog heeft.
    of blokeert de kaart als het er 0 zijn.

    returns loginstatus.pincode_invoeren als de gebruikers kaart niet is geblokeerd.
    ander loginstatus.geblokeerde_kaart
    """
    pogingen = userdata.pogingen
    if userdata.pogingen == 0:
        return LoginStatus.geblokeerde_kaart
    if isinstance(pogingen,str):
        return LoginStatus.kaartscan_fout
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Fout pincode.html", "r", "utf-8").read(), namespace='/test')
    socketio.emit('number', pogingen, namespace='/test')
    userdata.clearpin()
    sleep(1)
    return LoginStatus.pincode_invoeren

def inlogScherm()-> LoginStatus:
    """
    Functie voor het weergeven van het hoofdmenu scherm.
    Dit scherm geeft de gebruiker keuze uit verschillende handelingen
    door te kiezen uit een van deze opties:
    A: Saldo zien
    B: Snelopnemen 70 euro
    C: Zelf bedrag kiezen
    D: Transactie afbreken

    returns een LoginStatus op basis van de door de gebruiker gemaakte keus.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Keuzemenu.html", "r", "utf-8").read(), namespace='/test')
    while True:
        char = numpad.getInput()
        if char == "D":
            return LoginStatus.annulerings_scherm
        elif char == "A":
            return LoginStatus.saldo_zien
        elif char == "C":
            return LoginStatus.zelf_bedrag_kiezen
        elif char == "B":
            status = userdata.setOpnameHoeveelheid(70)
            if status == 0:
                return LoginStatus.niet_voldoende_saldo
            else:
                return LoginStatus.comformatie_bedrag


def saldoZien()-> LoginStatus:
    """
    Functie voor het weergeven van het saldo scherm.
    Dit scherm laat het huidige saldo van de gebruiker zien en geeft de gebruiker keuzes
    door te kiezen uit een van deze opties:
    A: Terug naar hoofdmenu
    B: Bedrag kiezen
    C: 
    D: Transactie afbreken

    returns een LoginStatus op basis van de door de gebruiker gemaakte keus.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Saldo zien.html", "r", "utf-8").read(), namespace='/test')
    socketio.emit('number', userdata.getSaldo(), namespace='/test')
    while True:
        char = numpad.getInput()
        if char == "D":
            return LoginStatus.annulerings_scherm
        elif char == "A":
            return LoginStatus.inlog_scherm
        elif char == "B":
            return LoginStatus.zelf_bedrag_kiezen

def briefkeuze()-> LoginStatus:
    """
    Functie voor het weergeven van het Briefkeuze scherm.
    Dit scherm geeft de gebruiker 3 keuzes in briefjes om het bedrag op te nemen
    door te kiezen uit een van deze opties:
    A: Briefkeuze A
    B: Briefkeuze B
    C: Briefkeuze C
    D: Transactie afbreken

    returns een LoginStatus op basis van de door de gebruiker gemaakte keus.
    """
    geld.geldkeuze(userdata.getopname())
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/briefkeuze.html", "r", "utf-8").read(), namespace='/test')
    socketio.emit('number', geld.makehtml(), namespace='/test')
    while True:
        char = numpad.getInput()
        if char == "D":
            return LoginStatus.annulerings_scherm
        elif char == "B":
            return LoginStatus.comformatie_bedrag
        elif char == "C":
            return LoginStatus.comformatie_bedrag
        elif char == "A":
            return LoginStatus.comformatie_bedrag

def zelfBedragKiezen()-> LoginStatus:
    """
    Functie voor het weergeven van het niet zelf bedrag kiezen scherm.
    Dit scherm geeft de gebruiker de mogelijkhijd om zelf een bedrag te kiezen door 
    middel van deze opties:
    0-9: getal aan het bedrag toevoegen
    A: Terug naar hoofdemenu
    B: Huidige bedrag opnemen
    C: Laatste getal weghalen
    D: Transactie afbreken

    returns een LoginStatus op basis van de door de gebruiker gemaakte keus.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Bedragkiezen.html", "r", "utf-8").read(), namespace='/test')
    bedrag = 0
    while True:
        sleep(0.3)
        char = numpad.getInput()
        if char == "D":
            return LoginStatus.annulerings_scherm
        elif char == "A":
            return LoginStatus.inlog_scherm
        elif char == "C":
            bedrag = int(bedrag/10)
            socketio.emit('number', bedrag, namespace='/test')
        elif char == "B":
            if bedrag <10:
                bedrag = 10
                socketio.emit('number', "bedrag afgerond naar: €"   + str(bedrag), namespace='/test')
                sleep(2)
            if bedrag % 10 != 0:
                bedrag = bedrag - (bedrag % 10)
                socketio.emit('number', "bedrag afgerond naar: €"   + str(bedrag), namespace='/test')
                sleep(2)
            status = userdata.setOpnameHoeveelheid(bedrag)
            if status == 0:
                return LoginStatus.niet_voldoende_saldo
            else:
                return LoginStatus.brief_keuze
        elif char == "A" or char =="B" or char =="C" or char=="#" or char == "*":
            pass
        else:
            bedrag = bedrag *10 + int(char)
            if bedrag > 300:
                bedrag = 300
            socketio.emit('number', bedrag, namespace='/test')



def NietVoldoendeSaldo()-> LoginStatus:
    """
    Functie voor het weergeven van het niet voldoende scherm.
    Dit scherm word weergeven als de gebruiker te weinig saldo geeft voor een transactie.
    Hierna heft de gebruiker een aantal keuzes:
    A: Saldo zien
    B: ander bedrag kiezen
    C: Terug naar hoofdemenu
    D: transactie afbreken

    returns een LoginStatus op basis van de door de gebruiker gemaakte keus.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/NietVoldoendeSaldo.html", "r", "utf-8").read(), namespace='/test')
    while True:
        char = numpad.getInput()
        if char == "D":
            return LoginStatus.annulerings_scherm
        elif char == "A":
            return LoginStatus.saldo_zien
        elif char == "B":
            return LoginStatus.zelf_bedrag_kiezen
        elif char == "C":
            return LoginStatus.inlog_scherm



def comformatieScherm()-> LoginStatus:
    """
    Functie voor het weergeven van het comformatie scherm.
    Dit scherm laat het bedrag zien dat de gebruiker gaat opnemen en de keuzes of dit klopt.
    A: terug naar het hoofdmenu
    B: transactie comformeren
    C: ander bedrag kiezen
    D: transactie afbreken

    returns een LoginStatus op basis van de door de gebruiker gemaakte keus.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Comformatiescherm.html", "r", "utf-8").read(), namespace='/test')
    socketio.emit('number', userdata.getopname(), namespace='/test')
    while True:
        char = numpad.getInput()
        if char == "D":
            return LoginStatus.annulerings_scherm
        elif char == "B":
            return LoginStatus.bedank_scherm
        elif char == "C":
            return LoginStatus.zelf_bedrag_kiezen
        elif char == "A":
            return LoginStatus.inlog_scherm

def bedankScherm()-> LoginStatus:
    """
    Functie voor het weergeven van het bedankt scherm scherm.
    Deze functie geeft de bon en het geld uit.
    Daarnaast leegt deze functie alle data van de huidige transactie.

    returns LoginStatus.scan_pas om terug te gaan naar het kaartscan scherm.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/BedankScherm.html", "r", "utf-8").read(), namespace='/test')
    val = userdata.updatesaldo()
    bon.printUserData(str(userdata.getIban()),"hans",str(userdata.getopname()))
    if val == 0:
        return LoginStatus.fout_scherm
    userdata.clearUserData()
    return LoginStatus.scan_pas

def annuleringsScherm()-> LoginStatus:
    """
    Functie voor het weergeven van het fout scherm.
    Daarnaast leegt deze functie alle data van de huidige transactie.

    returns LoginStatus.scan_pas om terug te gaan naar het kaartscan scherm.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Annuleringsscherm.html", "r", "utf-8").read(), namespace='/test')
    userdata.clearUserData()
    sleep(3)
    return LoginStatus.scan_pas

def foutScherm()-> LoginStatus:
    """
    Functie voor het weergeven van het fout scherm.
    Daarnaast leegt deze functie alle data van de huidige transactie.

    returns LoginStatus.scan_pas om terug te gaan naar het kaartscan scherm.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Fout bij scan.html", "r", "utf-8").read(), namespace='/test')
    userdata.clearUserData()
    sleep(3)
    return LoginStatus.scan_pas

def bonKeuze()-> LoginStatus:
    """
    Functie voor het weergeven van het bonkeuze scherm.
    Dit scherm geeft de gebruiker een keuze of die een bon wilt hebben.
    Ook kan de gebruiker de transactie afbreken of terug naar het hoofdemenu.

    returns een LoginStatus op basis van de door de gebruiker gemaakte keus.
    """
    return

def kaartscanfout()-> LoginStatus:
    """
    Functie voor het weergeven van het kaartscan fout scherm.
    Daarnaast leegt deze functie alle data van de huidige transactie.

    returns LoginStatus.scan_pas om terug te gaan naar het kaartscan scherm.
    """
    socketio.emit('pageinfo', codecs.open("/home/bluearrow8/Documents/project-bank/templates/Fout bij scan.html", "r", "utf-8").read(), namespace='/test')
    userdata.clearUserData()
    sleep(3)
    return LoginStatus.scan_pas




def loop():
    """
    Background task die regelt welk scherm de gebruiker te zoen krijgt
    """
    
    loginStatus = LoginStatus.scan_pas
    while True:
        
        sleep(0.4) #delay zodat als mensen langer hun vinger op de toetsen houden ze niet meerdere keuzes maken
        switcher = {
            1: scanPas,
            2: verwerkenKaart,
            3: kaartscanfout,
            4: geblokeerdeKaart,
            5: pincodeInvoer,
            6 : foutePincode,
            7: inlogScherm,
            8: saldoZien,
            9: briefkeuze,
            10: zelfBedragKiezen,
            11: NietVoldoendeSaldo,
            12: comformatieScherm,
            13: bedankScherm,
            14: annuleringsScherm,
            15: foutScherm,
            16: bonKeuze
        }
        # Get the function from switcher dictionary
        func = switcher.get(loginStatus.value, lambda: "invalid input")
        # Execute the function
        loginStatus = func()
        
        
       
          
        


if __name__ == '__main__':
    print("start")
    thread = socketio.start_background_task(loop)
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False)
    
    
    


    

