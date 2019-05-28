from tools import Tools
from datetime import date

#--------------------------------------------------
    # class Stunde creates objects from all other
    # classes --> timetables can be read lesson
    # by lesson
#--------------------------------------------------
class Stunde:

    Stundenliste = []
    StundenlisteMontag = []
    StundenlisteDienstag = []
    StundenlisteMittwoch = []
    StundenlisteDonnerstag = []
    StundenlisteFreitag = []

    #--------------------------------------------------
        # attributes:
        #   klasse (str): 5a,5b,...,1m1,1pas,qinf,...,2m1,... (case-sensitive!)
        #   lehrer (str): Eindeutiges Kuerzel; Poll,PorU,... (case-sensitive!)
        #   fach (str): Eindeutiges Kuerzel; Ph,B,Inf,... (case-sensitive!)
        #   woche (int): 0 = A & B Woche; 1 = A Woche; 2 = B Woche
        #   tag (int): 0 = Montag,..., 4 = Freitag
        #   stunde (int): 0 = 1.Stunde, 1 = 2.Stunde,..., 6 = 7.Stunde (Mittagspause),...,10 = 11.Stunde
    #--------------------------------------------------
    def __init__(self,klasse:str,raum:str,lehrer:str,fach:str,tag:int,stunde:int,ersatzstunde=False):
        self.klasse = Klasse.createKlasse(klasse,self)
        self.raum = Raum.createRaum(raum,self)
        self.lehrer = Lehrer.createLehrer(lehrer,self)
        self.fach = Fach.createFach(fach)
        #self.wochentyp = woche # A-week/B-week
        self.tag = tag
        self.stunde = stunde
        if not ersatzstunde:
            Stunde.Stundenliste.append(self)
            if tag == 0:
                Stunde.StundenlisteMontag.append(self)
            elif tag == 1:
                Stunde.StundenlisteDienstag.append(self)
            elif tag == 2:
                Stunde.StundenlisteMittwoch.append(self)
            elif tag == 3:
                Stunde.StundenlisteDonnerstag.append(self)
            elif tag == 4:
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
class Klasse:


    Klassenliste = []


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


    def __init__(self,bezeichner,stunde):
        self.stundenliste = []
        self.stundenplan = [[],[],[],[],[]]
        self.bezeichner = bezeichner

        Klasse.Klassenliste.append(self)
        self.addStunde(stunde)
        
    
    def addStunde(self,stunde):
        self.stundenliste.append(stunde)
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)
#--------------------------------------------------
#--------------------------------------------------


# #--------------------------------------------------
    # #--------------------------------------------------
    # class Kurs(Klasse):
    #     def __init__(self):
    #         pass
    # #--------------------------------------------------
# #--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Raum:


    Raumliste = []


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


    def __init__(self,bezeichner,stunde):
        self.bezeichner = bezeichner
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
class Lehrer:


    Lehrerliste = []


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


    def __init__(self,bezeichner,stunde):
        self.bezeichner = bezeichner
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
    
    def addBlockiert(self,tag,von,bis):
        self.blockiert.append(Blockierung(self,tag,von,bis))
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
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