
from typing import Union
from apiconnect import apiconnect


class UserData(apiconnect):
    """
    Class die word gebruikt als tijdelijke opslag voor dasta tijdens de transactie.
    """
    iban = None
    pincode = ""
    saldo = None
    pogingen = 0
    opnamehoeveelheid = None
    api = apiconnect()
    
    
    def clearUserData(self) -> None:
        """
        Functie voor het legen van alle user data van de huidige transactie.
        """
        self.iban =None
        self.pincode=""
        self.saldo= None
        self.pogingen = 0
        self.opnamehoeveelheid = None
    
    
    def clearpin(self)-> None:
        """
        functie voor het legen van de ingevoerde pincode na het invoeren van een verkeerde pincode.
        """
        self.pincode = ""

    def setIban(self,iban)-> int:
        """
        Functie voor het toevoegen van een iban voor de transactie.
        checked ook of de iban de juiste lengt heeft

        iban: Iban van de rekening waarin de transactie gaat plaatsvinden

        returns 1 voor succes of 0 voor als de iban lengte niet klopt
        """
        if len(iban) != 16:
            return 0
        
        self.iban = iban
        return 1

    
    def checkpincode(self)-> Union[int, str]:
        """
        Functie voor het controleren van de pincode via de API en het updaten van het saldo als deze correct is

        returns 1 voor succes of een string als er een fout is.
        """
        status, val = self.api.checksaldo(self.iban,self.pincode)
        if status == "foute pincode":
            self.pogingen = val
            return 0
        if status == "something went wrong":
            return status
        if status == "Pas geblokeerd":
            self.pogingen = val
            return 0
            
        else:
            self.saldo = float(val)
            return 1

    
    def addPincodeNumber(self,number) -> None:
        """
        functie voor het toevoegen van een nummer aan de pincode.
        """
        self.pincode = self.pincode + str(int(number))

    def removePincodeNumber(self) -> None:
        """
        functie voor het verwijderen van een nummer aan de pincode.
        """
        self.pincode = self.pincode[0:(len(self.pincode)-1)] 

    
    def checkPinSize(self) -> int:
        """
        Functie die de lenge van de pincode checked om te kijken of er een volledige pincode is ingevoerd

        Returnst 1 als de pincode volledig is ingevoert.
        anders 0
        """
        if len(self.pincode) == 4:
            return 1
        else:
            return 0


    def setOpnameHoeveelheid(self,hoeveelheid)-> int:
        """
        functie voor het registeren van het bedrag dat de klant wil opnemen.
        checked eerst of de klant genoeg saldo heeft om dit bedrag op te nemen.

        hoeveelheid: Hoeveelheid geld dat de klant wil opnemen

        returns 1 voor succes
        returns 0 voor te weinig saldo
        """
        if int(hoeveelheid) > int(self.saldo):
            return 0
        self.opnamehoeveelheid = hoeveelheid
        return 1
    
   
    def updatesaldo(self) -> bool:
        """
        functie voor het updaten van het saldo bij de bankservers.

        returns een boolean die het succes aangeeft.
        """
        status, val = self.api.withdrawl(self.iban, self.pincode, int(self.opnamehoeveelheid))
        if status == "foute pincode":
            if val == 0:
                status = "Pas geblokeerd"
            else:
                return val
        if status == "something went wrong":
            return 0
        if status == "Pas geblokeerd":
            return 0
        else:
            return val

   
    def getpincodepogingen(self)-> Union[int, str]:
        """
        Functie vor het opvragen van de pincodepoginen van de landserver API.
        Vraagt het aantal pogingen op van de iban die momenteel in het object staat geschreven

        Returned bij succes het aantal pogingen.
        Anders een error string.
        """

        pogingen = self.api.getpogingen(self.iban)
        if isinstance(pogingen,str):
            return 3
        
        return pogingen

   
    def getIban(self):
        return self.iban

  
    def getpincode(self):
        return self.pincode


    def getSaldo(self):
        return self.saldo

 
    def getopname(self):
        return self.opnamehoeveelheid

    
        
    
    
    
  

