from typing import Union
import requests
import json
class apiconnect:
    """
    Class voor het regelen van alle API calls naar de bankserver
    """
    
    def getpogingen(self,iban) -> Union[int, str]:
        """
        Functie voor het opvragen van het aantal pogingen die de rekening behorend tot de iban heeft voor deze geblokeerd word via de API.

        iban = Iban van de rekening waarvan de pogingen word opgevraagt.

        Returns het aantal pogingen of een error string.
        """
        URL = "http://145.24.222.179:80/api/pogingen"
        header = {
                'fromCtry': "test",
                'fromBank': "something",
                'toCtry':   iban[0:2],
                'toBank':   iban[2:6]
            }
        body = {"acctNo" : iban}
        try:
            payload = {'head':  header,'body':  body }
            r = requests.post(url = URL, json = payload)
            data = r.json()
            return data["body"]["pogingen"]
        except:
            return "something went wrong"


    def checksaldo(self, iban, pincode)-> Union[int, str]:
        """
        Functie voor het opvragen van het saldo behorend tot de rekening via de api

        iban = Iban van de rekening waarvan het saldo word opgevraagt.
        pincode = Pincode die gevarifieert moet worden met de pincode die in de database staat opgeslagen.

        returns het saldo of een error string.
        """
        
        URL = "http://145.24.222.179:80/balance"
        header = {
                'fromCtry': "GL",
                'fromBank': "BAOV",
                'toCtry':   iban[0:2],
                'toBank':   iban[2:6]
            }
        body = {"acctNo" : iban, "pin" : pincode}
        payload = {'head':  header,'body':  body }
        try:
            
            r = requests.post(url = URL, json = payload)
            print(r.status_code)
            
            data = r.json()
            print(data)
            if r.status_code == 401:
                return "foute pincode", int(data["body"]["attemptsLeft"])
            if r.status_code == 400:
                return "something went wrong",0
            if r.status_code == 404:
                return "something went wrong",0
            if r.status_code == 403:
                return "Pas geblokeerd",0

            
            
            
            return "succes" ,float(data["body"]["balance"])
        except:
            return "something went wrong",0

    def withdrawl(self, iban,pincode,hoeveelheid) -> bool:
        """
        Functie voor afschrijven van geld van de rekening behorend tot de iban via de api.

        iban = Iban van de rekening waarvan het geld moet worden afgeschreven.
        pincode = Pincode die gevarifieert moet worden met de pincode die in de database staat opgeslagen.
        hoeveelheid = hoeveelheid geld dat van de rekening afgeschreven moet worden

        returns een boolean of het geld van de rekening af halen gelukt is.
        """
       
        URL = "http://145.24.222.179:80/withdraw"
        header = {
                'fromCtry': "GL",
                'fromBank': "BAOV",
                'toCtry':   iban[0:2],
                'toBank':   iban[2:6]
            }
        body = {"acctNo" : iban, "pin" : pincode, "amount" : hoeveelheid}
        payload = {'head':  header,'body':  body }
        try:
            
            r = requests.post(url = URL, json = payload)
            data = r.json()
            print(data)
            print(r.status_code)
            if r.status_code == 401:
                return "foute pincode", data["body"]["attemptsLeft"]
            if r.status_code == 400:
                return "something went wrong",0
            if r.status_code == 404:
                return "something went wrong",0
            if r.status_code == 403:
                return "Pas geblokeerd",0
            if r.status_code == 406:
                return "Pas geblokeerd",0
            
            return "succes",data["body"]["success"]
        except:
            return "something went wrong",0


    def createrekening(self, iban, pincode, email)-> int:
        """
        Functie voor het aanmaken van een rekening  via de API.

        iban = Iban die de rekening die aangemaakt gaat worden gaat krijgen.
        pincode = pincode die de rekening die aangemaakt gaat worden gaat krijgen.
        Email = Email van het account waar de aangemaakte rekening aan gekopelt gaat worden.

        returns een boolean of het geld van de rekening af halen gelukt is.
        """
        URL = "http://145.24.222.179:80/api/createrekening"
        header = {"tobank" : "baov", "frombank" : "baov"}
        body = {"acctNo" : iban, "pin" : pincode, "email" :email}
        payload = {'head':  header,'body':  body }
        try:
            r = requests.post(url = URL, json = payload)
            data = r.json()
            return data
        except:
            return 0


