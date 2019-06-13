from PyQt5.QtCore import QDate
from tools import Tools

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

        if ersatzstunde and datum is not None:
            Stunde.Ersatzstundenliste.append(self)
            Stunde.Ersatzstundenliste.sort(key = lambda c: c.datum)
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Stunde.Stundenliste:
            del i
        for i in Stunde.StundenlisteMontag:
            del i
        for i in Stunde.StundenlisteDienstag:
            del i
        for i in Stunde.StundenlisteMittwoch:
            del i
        for i in Stunde.StundenlisteDonnerstag:
            del i
        for i in Stunde.StundenlisteFreitag:
            del i
        for i in Stunde.Ersatzstundenliste:
            del i
        Stunde.Stundenliste.clear()
        Stunde.StundenlisteMontag.clear()
        Stunde.StundenlisteDienstag.clear()
        Stunde.StundenlisteMittwoch.clear()
        Stunde.StundenlisteDonnerstag.clear()
        Stunde.StundenlisteFreitag.clear()
        Stunde.Ersatzstundenliste.clear()
    #--------------------------------------------------


    #--------------------------------------------------
    def __str__(self):
        s = str(self.tag) + ";" + str(self.stunde) + ";" + str(self.klasse) + ";" + str(self.lehrer) + ";" + str(self.raum) + ";" + str(self.fach)
        return s
    def __eq__(self,other):
        a = self.klasse == other.Klasse()
        b = self.tag == other.Tag()
        c = self.stunde == other.Stunde()
        # d = self.lehrer == other.Lehrer()
        # e = self.fach == other.Fach()
        if a and b and c:
            return True
        else:
            return False
    def __lt__(self,other):
        a = self.klasse < other.Klasse()
        b = self.tag < other.Tag()
        c = self.stunde < other.Stunde()

        if a:
            return a
        if b:
            return b
        if c:
            return c
        return False
    #--------------------------------------------------


    #--------------------------------------------------
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
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def getStundenliste():
        return Stunde.Stundenliste
    #--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Klasse:


    Klassenliste = []

    #--------------------------------------------------
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
    #--------------------------------------------------


    #--------------------------------------------------
    def __init__(self,bezeichner:str,stunde:Stunde):
        self.bezeichner = bezeichner

        self.stundenliste = []
        self.stundenplan = [[],[],[],[],[]]
        self.lehrerliste = []

        Klasse.Klassenliste.append(self)
        self.addStunde(stunde)
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Klasse.Klassenliste:
            del i
        Klasse.Klassenliste.clear()
    #--------------------------------------------------


    #--------------------------------------------------
    def __str__(self):
        return self.bezeichner
    def __eq__(self,other):
        return self.bezeichner==other.Bezeichner()
    def __lt__(self,other):
        return self.bezeichner < other.Bezeichner()
    #--------------------------------------------------


    #--------------------------------------------------
    def addStunde(self,stunde:Stunde):
        self.stundenliste.append(stunde)
        self.addLehrer(stunde.Lehrer())
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)
    def addLehrer(self,lehrer): #(self,lehrer:Lehrer)
        if lehrer not in self.lehrerliste:
            self.lehrerliste.append(lehrer)
    #--------------------------------------------------


    #--------------------------------------------------
    def Bezeichner(self):
        return self.bezeichner
    #--------------------------------------------------
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
        if stunde != "":
            self.addStunde(stunde)


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Raum.Raumliste:
            del i
        Raum.Raumliste.clear()
    #--------------------------------------------------


    def __str__(self):
        return self.bezeichner
    def __eq__(self,other):
        return self.bezeichner==other.Bezeichner()
    def __lt__(self,other):
        return self.bezeichner < other.Bezeichner()


    def addStunde(self,stunde:Stunde):
        self.stundenliste.append(stunde)
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)

    def addBlockiert(self,datum,von:int,bis:int): #(self,datum:Tag,von:int,bis:int)
        self.blockiert.append(Blockierung(self,datum,von,bis))


    def Bezeichner(self):
        return self.bezeichner

    @staticmethod
    def RaumListe():
        return Raum.Raumliste
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


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Lehrer.Lehrerliste:
            del i
        Lehrer.Lehrerliste.clear()
    #--------------------------------------------------


    def __str__(self):
        return self.bezeichner
    def __eq__(self,other):
        return self.bezeichner==other.Bezeichner()
    def __lt__(self,other):
        return self.bezeichner < other.Bezeichner()


    def addStunde(self,stunde:Stunde):
        self.stundenliste.append(stunde)
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)

        # automatically add fach to faecherliste if not already in it
        if stunde.Fach() not in self.faecherliste:
            self.faecherliste.append(stunde.Fach())

    def addBlockiert(self,datum,von:int,bis:int): #(self,datum:Tag,von:int,bis:int)
        self.blockiert.append(Blockierung(self,datum,von,bis))
        self.blockiert.sort()
    def Blockiert(self):
        return self.blockiert


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


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Fach.Fachliste:
            del i
        Fach.Fachliste.clear()
    #--------------------------------------------------


    def __str__(self):
        return self.bezeichner
    def __eq__(self,other):
        return self.bezeichner == other.Bezeichner()
    def __lt__(self,other):
        return self.bezeichner < other.Bezeichner()


    def Bezeichner(self):
        return self.bezeichner
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Tag(QDate):

    tagListe = []

    @staticmethod #create static method that can be called without object
    # method checks for already existing object and either returns the existing or creates a new one and returns this
    def createTag(qdate:QDate):
        if qdate not in Tag.tagListe:
            return Tag(qdate)
        else:
            for element in Tag.tagListe:
                if element == qdate:
                    return element

    def __init__(self,qdate:QDate):
        super().__init__(qdate)
        self.blockierteLehrer = []
        self.blockierteRaeume = []
        self.ersatzstunden = []
        Tag.tagListe.append(self)


        if self.dayOfWeek()-1 == 0:
            self.stunden = Stunde.StundenlisteMontag
        elif self.dayOfWeek()-1 == 1:
            self.stunden = Stunde.StundenlisteDienstag
        elif self.dayOfWeek()-1 == 2:
            self.stunden = Stunde.StundenlisteMittwoch
        elif self.dayOfWeek()-1 == 3:
            self.stunden = Stunde.StundenlisteDonnerstag
        elif self.dayOfWeek()-1 == 4:
            self.stunden = Stunde.StundenlisteFreitag
        else:
            self.stunden = []


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Tag.tagListe:
            del i
        Tag.tagListe.clear()
    #--------------------------------------------------


    def __eq__(self,other):
        return self.getDate() == other.getDate()
    def __lt__(self,other):
        return self.getDate() < other.getDate()


    def addBlockierterLehrer(self,lehrer:Lehrer):
        if lehrer not in self.blockierteLehrer:
            # auf alte Blockierung pruefen, um Doppelung zu vermeiden
            self.blockierteLehrer.append(lehrer)
    def addBlockierterRaum(self,raum:Raum):
        if raum not in self.blockierteRaeume:
            # auf alte Blockierung pruefen, um Doppelung zu vermeiden
            self.blockierteRaeume.append(raum)
    def addErsatzstunde(self,stunde:Stunde):
        if stunde in self.stunden:
            self.stunden.remove(stunde) # Originalstunde aus Liste entfernen
        if stunde in self.ersatzstunden:
            # auf alte Vertretungsstunde pruefen, um Doppelung zu vermeiden
            self.ersatzstunden.remove(stunde)
        self.ersatzstunden.append(stunde)

    def BlockierteLehrer(self):
        return self.blockierteLehrer
    def BlockierteRaeume(self):
        return self.blockierteRaeume
    def Ersatzstunden(self):
        return self.ersatzstunden
    def Stunden(self):
        return self.stunden
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Blockierung:
    blockierteLehrer = []
    blockierteRaeume = []
    #--------------------------------------------------
        # attributes:
        #   tag: Tag object
        #   von/bis: 0-10; if bis is smaller than von bis is replaced by 10 (end of day)
    #--------------------------------------------------
    def __init__(self,blockiertesObject,datum:Tag,von:int,bis:int):
        self.blockiertesObjekt = blockiertesObject
        self.datum = datum
        self.von = von
        if bis < von:
            self.bis = 10
        else:
            self.bis = bis

        if isinstance(self.blockiertesObjekt,Lehrer):
            self.datum.addBlockierterLehrer(self.blockiertesObjekt)
            Blockierung.blockierteLehrer.append(self)
        elif isinstance(self.blockiertesObjekt,Raum):
            self.datum.addBlockierterRaum(self.blockiertesObjekt)
            Blockierung.blockierteRaeume.append(self)


    #--------------------------------------------------
    @staticmethod
    def clearData():
        Blockierung.blockierteLehrer.clear()
        Blockierung.blockierteRaeume.clear()
    #--------------------------------------------------

    def __str__(self):
        return str(self.blockiertesObjekt) + ";" + str(self.datum) + ";" + str(self.von) + ";" + str(self.bis)
    def __eq__(self, other):
        return self.blockiertesObjekt == other.BlockiertesObjekt()
    def __lt__(self,other):
        return self.blockiertesObjekt < other.BlockiertesObjekt()

    def BlockiertesObjekt(self):
        return self.blockiertesObjekt
    def Datum(self):
        return self.datum
    def Von(self):
        return self.von
    def Bis(self):
        return self.bis

    @staticmethod
    def BlockierteLehrer():
        return Blockierung.blockierteLehrer
    @staticmethod
    def BlockierteRaeume():
        return Blockierung.blockierteRaeume
#--------------------------------------------------
#--------------------------------------------------