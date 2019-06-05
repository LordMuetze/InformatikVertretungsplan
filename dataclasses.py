from tools import Tools
from datetime import date
from dataclasses import dataclass

#--------------------------------------------------
    # class Stunde creates objects from all other
    # classes --> timetables can be read lesson
    # by lesson
#--------------------------------------------------
@dataclass
class Stunde:

    Stundenliste = []
    StundenlisteMontag = []
    StundenlisteDienstag = []
    StundenlisteMittwoch = []
    StundenlisteDonnerstag = []
    StundenlisteFreitag = []

    klasse: Klasse
    raum: Raum
    lehrer: Lehrer
    fach: Fach
    tag: Tag
    stunde: Stunde
    ersatzstunde: bool = False

    #--------------------------------------------------
        # attributes:
        #   klasse (str): 5a,5b,...,1m1,1pas,qinf,...,2m1,... (case-sensitive!)
        #   lehrer (str): Eindeutiges Kuerzel; Poll,PorU,... (case-sensitive!)
        #   fach (str): Eindeutiges Kuerzel; Ph,B,Inf,... (case-sensitive!)
        #   woche (int): 0 = A & B Woche; 1 = A Woche; 2 = B Woche
        #   tag (int): 0 = Montag,..., 4 = Freitag
        #   stunde (int): 0 = 1.Stunde, 1 = 2.Stunde,..., 6 = 7.Stunde (Mittagspause),...,10 = 11.Stunde
    #--------------------------------------------------
    def __post_init__(self):
        if not self.ersatzstunde:
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
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
@dataclass
class Klasse:


    Klassenliste = []
    
    bezeichner:str
    stunde: Stunde
    stundenliste: list = []
    stundenplan: list = [[],[],[],[],[]]


    @staticmethod #create static method that can be called without object
    #method checks for already existing object and either returns the existing or creates a new one and returns this
    def createKlasse(bezeichner:str,stunde):
        if bezeichner not in list(map(lambda c: c.bezeichner,Klasse.Klassenliste)):
            return Klasse(bezeichner,stunde)
        else:
            for element in Klasse.Klassenliste:
                if element.bezeichner == bezeichner:
                    element.addStunde(stunde)
                    return element


    def __post_init__(self):
        Klasse.Klassenliste.append(self)
        self.addStunde(self.stunde)
        
    
    def addStunde(self,stunde):
        self.stundenliste.append(stunde)
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
@dataclass
class Raum:


    Raumliste = []

    bezeichner:str
    #stunde:Stunde


    @staticmethod #create static method that can be called without object
    #method checks for already existing object and either returns the existing or creates a new one and returns this
    def createRaum(bezeichner,stunde):
        if bezeichner not in list(map(lambda c: c.bezeichner,Raum.Raumliste)):
            return Raum(bezeichner,stunde)
        else:
            for element in Raum.Raumliste:
                if element.bezeichner == bezeichner:
                    element.addStunde(stunde)
                    return element


    def __post_init__(self,stunde):
        self.stundenliste = []
        self.stundenplan = [[],[],[],[],[]]
        self.blockiert = []

        Raum.Raumliste.append(self)
        self.addStunde(stunde)


    def addStunde(self,stunde):
        self.stundenliste.append(stunde)
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)
    
    def addBlockiert(self,tag,von,bis):
        self.blockiert.append(Blockierung(self,tag,von,bis))
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
@dataclass
class Lehrer:


    Lehrerliste = []

    bezeichner:str

    @staticmethod #create static method that can be called without object
    #method checks for already existing object and either returns the existing or creates a new one and returns this
    def createLehrer(bezeichner,stunde):
        if bezeichner not in list(map(lambda c: c.bezeichner,Lehrer.Lehrerliste)):
            return Lehrer(bezeichner,stunde)
        else:
            for element in Lehrer.Lehrerliste:
                if element.bezeichner == bezeichner:
                    element.addStunde(stunde)
                    return element


    def __post_init__(self,stunde):
        self.stundenliste = []
        self.stundenplan = [[],[],[],[],[]]
        self.absolvierteVertretungen = 0
        self.faecherliste = []

        Lehrer.Lehrerliste.append(self)
        self.addStunde(stunde)
        self.blockiert = []

    
    def addStunde(self,stunde):
        self.stundenliste.append(stunde)
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)

        # automatically add fach to faecherliste if not already in it
        if stunde.Fach() not in self.faecherliste:
            self.faecherliste.append(stunde.Fach())
    
    def addBlockiert(self,tag,von,bis):
        self.blockiert.append(Blockierung(self,tag,von,bis))
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
@dataclass
class Fach:


    Fachliste = []


    @staticmethod #create static method that can be called without object
    #method checks for already existing object and either returns the existing or creates a new one and returns this
    def createFach(bezeichner):
        if bezeichner not in list(map(lambda c: c.bezeichner,Fach.Fachliste)):
            return Fach(bezeichner)
        else:
            for element in Fach.Fachliste:
                if element.bezeichner == bezeichner:
                    return element


    def __init__(self,bezeichner):
        self.bezeichner = bezeichner
        Fach.Fachliste.append(self)
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


    def addBlockierterLehrer(self,lehrer):
        self.blockierteLehrer.append(lehrer)
    def addBlockierterRaum(self,raum):
        self.blockierteRaeume.append(raum)
    def addErsatzstunde(self,stunde):
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
    def __init__(self,blockiertesObject,tag:int,von:int,bis:int):
        self.tag = tag
        self.von = von
        if bis < von:
            self.bis = 10
        else:
            self.bis = bis

        if type(blockiertesObject) == Lehrer:
            self.tag.addBlockierterLehrer(blockiertesObject)
        elif type(blockiertesObject) == Raum:
            self.tag.addBlockierterRaum(blockiertesObject)
#--------------------------------------------------
#--------------------------------------------------