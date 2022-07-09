import RPi.GPIO as GPIO
from write import SimpleMFRC522
import json

class CardReader:
        """
        Class voor het schrijven en lezen van data naar de RFID
        """
        __reader = None
        __iban = None

        def __init__(self):
                GPIO.setwarnings(False)
                self.__reader = SimpleMFRC522()

        def writecard(self, rekeningNummer) -> bool:
                """
                Functie voor het schrijven van een iban op een kaart.
                de data word in block 1 van de rfid kaart geschreven

                rekeningNummer: laatste 8 nummers van de rekening die op de kaart gezet gaat worden.

                returns een boolean die aangeeft of het schrijven gelukt is.
                """
                try:   
                        iban = "GLBAOV0000" + str(rekeningNummer) + "00"
                        print("Now place your tag to write")
                        id,text = self.__reader.write(iban)
                        print(text)
                        return True
                except:
                        return False


        def checkcard(self)-> bool:
                """
                Functie voor het lezen van de iban van de kaart.
                de data word van block 1 van de rfid gelezen.
                De data die word gelezen word in het object geplaatst.

                returns een boolean of het lezen gelukt is.
                """
                try:
                        id,iban = self.__reader.read()
                        self.iban = iban
                        return True
                except:
                        return False

        
        def getiban(self) -> str:
                """returns de iban van de laatst gescande kaart in string formaat"""
                return self.iban
                

  

GPIO.cleanup()

