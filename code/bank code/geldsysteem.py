


class moneydispenser:
    """
    Class voor het bijhouden van het geld in het ATM, calculeren van briefkeuzes en het uitgeven van het geld
    """
    geldkeuzes = {"A": {}, "B" : {}, "C"  : {}}
    vijftig = 5
    twintig = 0
    tien = 30
    vijf = 0

    def __init__(self):
            return

    def geldkeuze(self, hoeveelheid) -> None:
        """
        Functie voor het berekenen van 3 geldkeuzes.
        De eerste keuze is zo veel mogelijk briefjes van 50
        De tweede keuze is 50/50
        de 3de keus is voornamelijk briefjes van 10 zo ver dat mogelijk is
        de 3 keuzes worden opgeslagen in het object zelf

        hoeveelheid: Het gekozen bedrag om op te nemen
        """
        
        self.geldkeuzes["A"]["vijftig"] = int(hoeveelheid / 50) 
        self.geldkeuzes["A"]["tien"] = int(hoeveelheid % 50 /10)
        if self.geldkeuzes["A"]["vijftig"] > self.vijftig or self.geldkeuzes["A"]["tien"] > self.tien:
            self.geldkeuzes["A"] = "Niet mogelijk"
    

        self.geldkeuzes["B"]["vijftig"] = int(hoeveelheid / 2 / 50)
        self.geldkeuzes["B"]["tien"] = int((hoeveelheid - self.geldkeuzes["B"]["vijftig"] * 50) / 10) 
        if self.geldkeuzes["B"]["vijftig"] > self.vijftig or self.geldkeuzes["B"]["tien"] > self.tien:
            self.geldkeuzes["B"] = "Niet mogelijk"

        self.geldkeuzes["C"]["vijftig"] = 0
        self.geldkeuzes["C"]["tien"] = int(hoeveelheid / 10) 
        if self.geldkeuzes["C"]["vijftig"] > self.vijftig or self.geldkeuzes["C"]["tien"] > self.tien:
            self.geldkeuzes["C"] = "Niet mogelijk"

        print("\n" + str(self.geldkeuzes["A"]) + "\n")
        print(str(self.geldkeuzes["B"])+ "\n")
        print(str(self.geldkeuzes["C"]) + "\n")
        
    def makehtml(self) -> str:
        """
        Functie voor het maken van een html voor de GUI van de ATM.
        Deze functie maakt deze html op basis van de geldkeuzes die zijn gemaakt in de geldkeuze() functie.
        """
        html = ""
        header = """<div class="element-option-1">
                <div class="element-option-text-1"> {}</div>
                <div class="element-option-input-1">{}</div>
            </div>"""
        for element in self.geldkeuzes:
            if self.geldkeuzes[element] == "Niet mogelijk":
                html = html
            else:
                numbers = "50x " + str(self.geldkeuzes[element]["vijftig"]) + " & 10x " + str(self.geldkeuzes[element]["tien"])
                html += header.format(numbers , element)

        html += """<div class="element-option-1">
                <div class="element-option-text-1">Afbreken</div>
                <div class="element-option-input-1">D</div>
            </div>"""
        print(html)
        return html
    
    def gelduitgeven(keuze):
        """
        Placeholder voor de functie die daadwerkelijk het geld uit gaat geven
        """
        return
    

        




    

