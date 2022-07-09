from escpos.printer import Serial
from time import *
from datetime import date
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%b/%d/%Y %H:%M:%S")
print("Today's date:", dt_string)

class bonprinter:
    def printUserData(self, iban, naam, opnamehoeveelheid):
        p = Serial(devfile='/dev/serial0',
                baudrate=9600,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1.00,
                dsrdtr=True)
        p.set(
            align="left",
            font="a",
            width=1,
            height=1,
            density=3,
            invert=0,
            smooth=False,
            flip=False,
    )
        p.text("BANKOVERVAL\n")
        p.text("DATE : ")
        p.text(dt_string + "\n")
        p.text("Naam : " +naam+ "\n")
        p.text("IBAN : "+ iban+ "\n")
        
        p.text("U heeft " + opnamehoeveelheid+ " euro opgenomen" +  "\n")
        p.text("\nDankuwel voor het pinnen")
        p.text("\nbij bankoverval")
        p.text("\n\n\n\n")

    def printDate(self):
        p = Serial(devfile='/dev/serial0',
                baudrate=19200,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1.00,
                dsrdtr=True)
        p.set(
            align="left",
            font="a",
            width=1,
            height=2,
            density=3,
            invert=0,
            smooth=False,
            flip=False,
    )
        p.text("DATE : ")
        p.text(dt_string)

