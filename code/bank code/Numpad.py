import RPi.GPIO as GPIO
import time

class Numpad:
    """
    Class voor het laten werken van de Numpad.
    de numpad moet van links naar rechts worden aangesloten op pin:
        5,6,13,19,12,16,20,21
    """
    L1 = 5
    L2 = 6
    L3 = 13
    L4 = 19

    C1 = 12
    C2 = 16
    C3 = 20
    C4 = 21

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.L1, GPIO.OUT)
        GPIO.setup(self.L2, GPIO.OUT)
        GPIO.setup(self.L3, GPIO.OUT)
        GPIO.setup(self.L4, GPIO.OUT)

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def readLine(self,line, characters):
        """
        Functie voor het uitlezen van de horizontalen lijnen van de numpad.

        line: De pin waarop de line zit aangesloten.
        characters: array van de symbolen die op deze line zitten.
        """
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.C1) == 1):
            return characters[0]
        if(GPIO.input(self.C2) == 1):
            return characters[1]
        if(GPIO.input(self.C3) == 1):
            return characters[2]
        if(GPIO.input(self.C4) == 1):
            return characters[3]
        GPIO.output(line, GPIO.LOW)
        return None

    def getInput(self) ->str:
        """
        Functie voor het uitlezen van de numpad.
        Als deze functie word geroepen maar 1 minuut lang geen input krijgt zal deze "D" returnen wat staat voor transactie afbreken
        """
        try:
            i = 0
            while i < 600:
                time.sleep(0.1)
                i = i+ 1
                
                char = self.readLine(self.L1, ["1","2","3","A"])
                if char != None:
                    return char
                char = self.readLine(self.L2, ["4","5","6","B"])
                if char != None:
                    return char
                char = self.readLine(self.L3, ["7","8","9","C"])
                if char != None:
                    return char
                char = self.readLine(self.L4, ["*","0","#","D"])
                if char != None:
                    return char
            return "D"
        except KeyboardInterrupt:
            print("\nApplication stopped!")
            GPIO.cleanup()

