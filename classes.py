from tools import Tools
from datetime import date

#--------------------------------------------------
    # class Stunde creates objects from all other
    # classes --> schedules can be read lesson by lesson
#--------------------------------------------------
class Stunde:

    Stundenliste = []
    StundenlisteMontag = []
    StundenlisteDienstag = []
    StundenlisteMittwoch = []
    StundenlisteDonnerstag = []
    StundenlisteFreitag = []
    Ersatzstundenliste = []

    #--------------------------------------------------
        # attributes:
        #   klasse (str): 5a,5b,...,1m1,1pas,qinf,...,2m1,... (case-sensitive!)
        #   lehrer (str): Eindeutiges Kuerzel; Poll,PorU,... (case-sensitive!)
        #   fach (str): Eindeutiges Kuerzel; Ph,B,Inf,... (case-sensitive!)
        #   woche (int): 0 = A & B Woche; 1 = A Woche; 2 = B Woche
        #   tag (int): 0 = Montag,..., 4 = Freitag
        #   stunde (int): 0 = 1.Stunde, 1 = 2.Stunde,..., 6 = 7.Stunde (Mittagspause),...,10 = 11.Stunde
    #--------------------------------------------------
    def __init__(self,tag:int,stunde:int,klasse:str,lehrer:str,raum:str,fach:str,ersatzstunde=False,datum=None):
        self.tag = tag
        self.stunde = stunde
        self.fach = Fach.createFach(fach)
        self.lehrer = Lehrer.createLehrer(lehrer,self) #needs self.fach
        self.klasse = Klasse.createKlasse(klasse,self) #needs self.lehrer
        self.raum = Raum.createRaum(raum,self)
        
        
        
        #self.wochentyp = woche # A-week/B-week
        self.ersatzstunde = ersatzstunde
        self.datum = datum

        if not ersatzstunde:
            Stunde.Stundenliste.append(self)
            if self.tag == 0:
                Stunde.StundenlisteMontag.append(self)
            elif self.tag == 1:
                Stunde.StundenlisteDienstag.append(self)
            elif self.tag == 2:
                Stunde.StundenlisteMittwoch.append(self)
            elif self.tag == 3:
                Stunde.StundenlisteDonnerstag.append(self)
            elif self.tag == 4:
                Stunde.StundenlisteFreitag.append(self)
        
        if ersatzstunde and datum != None:
            Stunde.Ersatzstundenliste.append(self)
            Stunde.Ersatzstundenliste.sort(key = lambda c: c.datum)


    def __str__(self):
        s = str(self.tag) + "," + str(self.stunde) + "," + str(self.klasse) + "," + str(self.lehrer) + "," + str(self.raum) + "," + str(self.fach)
        return s


    def Stunde(self):
        return self.stunde
    def Tag(self):
        return self.tag
    def Klasse(self):
        return self.klasse
    def Raum(self):
        return self.raum
    def Lehrer(self):
        return self.lehrer
    def Fach(self):
        return self.fach
    def Ersatzstunde(self):
        return self.ersatzstunde
    def Datum(self):
        return self.datum

    @staticmethod
    def getStundenliste():
        return Stunde.Stundenliste
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Klasse:


    Klassenliste = []


    @staticmethod #create static method that can be called without object
    #method checks for already existing object and either returns the existing or creates a new one and returns this
    def createKlasse(bezeichner:str,stunde:Stunde):
        if bezeichner not in list(map(lambda c: c.bezeichner,Klasse.Klassenliste)):
            return Klasse(bezeichner,stunde)
        else:
            for element in Klasse.Klassenliste:
                if element.bezeichner == bezeichner:
                    element.addStunde(stunde)
                    return element


    def __init__(self,bezeichner:str,stunde:Stunde):
        self.bezeichner = bezeichner

        self.stundenliste = []
        self.stundenplan = [[],[],[],[],[]]
        self.lehrerliste = []
        
        Klasse.Klassenliste.append(self)
        self.addStunde(stunde)
    

    def __str__(self):
        return self.bezeichner
        
    
    def addStunde(self,stunde:Stunde):
        self.stundenliste.append(stunde)
        self.addLehrer(stunde.Lehrer())
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)
    def addLehrer(self,lehrer): #(self,lehrer:Lehrer)
        if lehrer not in self.lehrerliste:
            self.lehrerliste.append(lehrer)
    

    def Bezeichner(self):
        return self.bezeichner
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Raum:


    Raumliste = []


    @staticmethod #create static method that can be called without object
    #method checks for already existing object and either returns the existing or creates a new one and returns this
    def createRaum(bezeichner:str,stunde:Stunde):
        if bezeichner not in list(map(lambda c: c.bezeichner,Raum.Raumliste)):
            return Raum(bezeichner,stunde)
        else:
            for element in Raum.Raumliste:
                if element.bezeichner == bezeichner:
                    element.addStunde(stunde)
                    return element


    def __init__(self,bezeichner:str,stunde:Stunde):
        self.bezeichner = bezeichner

        self.stundenliste = []
        self.stundenplan = [[],[],[],[],[]]
        self.blockiert = []

        Raum.Raumliste.append(self)
        self.addStunde(stunde)


    def __str__(self):
        return self.bezeichner


    def addStunde(self,stunde:Stunde):
        self.stundenliste.append(stunde)
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)
    
    def addBlockiert(self,datum,von:int,bis:int): #(self,datum:Tag,von:int,bis:int)
        self.blockiert.append(Blockierung(self,datum,von,bis))
    

    def Bezeichner(self):
        return self.bezeichner
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Lehrer:


    Lehrerliste = []


    @staticmethod #create static method that can be called without object
    #method checks for already existing object and either returns the existing or creates a new one and returns this
    def createLehrer(bezeichner:str,stunde:Stunde):
        if bezeichner not in list(map(lambda c: c.bezeichner,Lehrer.Lehrerliste)):
            return Lehrer(bezeichner,stunde)
        else:
            for element in Lehrer.Lehrerliste:
                if element.bezeichner == bezeichner:
                    element.addStunde(stunde)
                    return element


    def __init__(self,bezeichner:str,stunde:Stunde):
        self.bezeichner = bezeichner

        self.stundenliste = []
        self.stundenplan = [[],[],[],[],[]]
        self.absolvierteVertretungen = 0
        self.faecherliste = []

        Lehrer.Lehrerliste.append(self)
        self.addStunde(stunde)
        self.blockiert = []


    def __str__(self):
        return self.bezeichner


    def addStunde(self,stunde:Stunde):
        self.stundenliste.append(stunde)
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)

        # automatically add fach to faecherliste if not already in it
        if stunde.Fach() not in self.faecherliste:
            self.faecherliste.append(stunde.Fach())
    
    def addBlockiert(self,datum,von:int,bis:int): #(self,datum:Tag,von:int,bis:int)
        self.blockiert.append(Blockierung(self,datum,von,bis))
    

    def Bezeichner(self):
        return self.bezeichner
    
    @staticmethod
    def LehrerListe():
        return Lehrer.Lehrerliste
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Fach:


    Fachliste = []


    @staticmethod #create static method that can be called without object
    #method checks for already existing object and either returns the existing or creates a new one and returns this
    def createFach(bezeichner:str):
        if bezeichner not in list(map(lambda c: c.bezeichner,Fach.Fachliste)):
            return Fach(bezeichner)
        else:
            for element in Fach.Fachliste:
                if element.bezeichner == bezeichner:
                    return element


    def __init__(self,bezeichner:str):
        self.bezeichner = bezeichner
        Fach.Fachliste.append(self)
    
    
    def __str__(self):
        return self.bezeichner
    

    def Bezeichner(self):
        return self.bezeichner
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Tag(date):
    def __init__(self,jahr:int,monat:int,tag:int):
        super().__init__()
        self.blockierteLehrer = []
        self.blockierteRaeume = []
        self.ersatzstunden = []

        if self.weekday() == 0:
            self.stunden = Stunde.StundenlisteMontag
        elif self.weekday() == 1:
            self.stunden = Stunde.StundenlisteDienstag
        elif self.weekday() == 2:
            self.stunden = Stunde.StundenlisteMittwoch
        elif self.weekday() == 3:
            self.stunden = Stunde.StundenlisteDonnerstag
        elif self.weekday() == 4:
            self.stunden = Stunde.StundenlisteFreitag
        else:
            self.stunden = []


    def addBlockierterLehrer(self,lehrer:Lehrer):
        self.blockierteLehrer.append(lehrer)
    def addBlockierterRaum(self,raum:Raum):
        self.blockierteRaeume.append(raum)
    def addErsatzstunde(self,stunde:Stunde):
        self.ersatzstunden.append(stunde)
        self.ersatzstunden.sort(key = lambda c: c.Klasse())
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Blockierung:
    #--------------------------------------------------
        # attributes:
        #   tag: Tag object
        #   von/bis: 0-10; if bis is smaller than von bis is replaced by 10 (end of day)
    #--------------------------------------------------
    def __init__(self,blockiertesObject,datum:Tag,von:int,bis:int):
        self.datum = datum
        self.von = von
        if bis < von:
            self.bis = 10
        else:
            self.bis = bis

        if type(blockiertesObject) == Lehrer:
            self.datum.addBlockierterLehrer(blockiertesObject)
        elif type(blockiertesObject) == Raum:
            self.datum.addBlockierterRaum(blockiertesObject)
#--------------------------------------------------
#--------------------------------------------------