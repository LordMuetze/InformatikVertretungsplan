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

    #--------------------------------------------------
        # attributes:
        #   klasse (str): 5a,5b,...,1m1,1pas,qinf,...,2m1,... (case-sensitive!)
        #   lehrer (str): Eindeutiges Kuerzel; Poll,PorU,... (case-sensitive!)
        #   fach (str): Eindeutiges Kuerzel; Ph,B,Inf,... (case-sensitive!)
        #   woche (int): 0 = A & B Woche; 1 = A Woche; 2 = B Woche
        #   tag (int): 0 = Montag,..., 4 = Freitag
        #   stunde (int): 0 = 1.Stunde, 1 = 2.Stunde,..., 6 = 7.Stunde (Mittagspause),...,10 = 11.Stunde
    #--------------------------------------------------
    def __init__(self,tag:int,stunde:int,klasse:str,lehrer:str,raum:str,fach:str,ersatzstunde=False):
        if fach[:2].isdigit():
            klasse = fach
            fach = fach[2:len(fach)-1]


        self.tag = tag
        self.stunde = stunde
        self.fach = Fach.createFach(fach)
        self.lehrer = Lehrer.createLehrer(lehrer,self) #needs self.fach
        self.klasse = Klasse.createKlasse(klasse,self) #needs self.lehrer
        self.raum = Raum.createRaum(raum,self)

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
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Stunde.Stundenliste:
            i.tag = None
            i.stunde = None
            i.lehrer = None
            i.fach = None
            i.raum = None
            i.klasse = None
            del i
        for i in Stunde.StundenlisteMontag:
            i.tag = None
            i.stunde = None
            i.lehrer = None
            i.fach = None
            i.raum = None
            i.klasse = None
            del i
        for i in Stunde.StundenlisteDienstag:
            i.tag = None
            i.stunde = None
            i.lehrer = None
            i.fach = None
            i.raum = None
            i.klasse = None
            del i
        for i in Stunde.StundenlisteMittwoch:
            i.tag = None
            i.stunde = None
            i.lehrer = None
            i.fach = None
            i.raum = None
            i.klasse = None
            del i
        for i in Stunde.StundenlisteDonnerstag:
            i.tag = None
            i.stunde = None
            i.lehrer = None
            i.fach = None
            i.raum = None
            i.klasse = None
            del i
        for i in Stunde.StundenlisteFreitag:
            i.tag = None
            i.stunde = None
            i.lehrer = None
            i.fach = None
            i.raum = None
            i.klasse = None
            del i
        Stunde.Stundenliste = []
        Stunde.StundenlisteMontag = []
        Stunde.StundenlisteDienstag = []
        Stunde.StundenlisteMittwoch = []
        Stunde.StundenlisteDonnerstag = []
        Stunde.StundenlisteFreitag = []
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
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def StundenListe():
        return Stunde.Stundenliste
    #--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Vertretungsstunde(Stunde):

    Vertretungsstundenliste = []

    #--------------------------------------------------
    def __init__(self,tag:int,stunde:int,klasse:str,lehrer:str,raum:str,fach:str,datum,bemerkung:str): #datum:Tag
        super().__init__(tag,stunde,klasse,lehrer,raum,fach,True)
        self.datum = datum
        self.bemerkung = bemerkung

        Vertretungsstunde.Vertretungsstundenliste.append(self)
        Vertretungsstunde.Vertretungsstundenliste.sort(key = lambda c: c.datum)
        self.datum.addErsatzstunde(self)
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Vertretungsstunde.Vertretungsstundenliste:
            del i
        Vertretungsstunde.Vertretungsstundenliste = []
    #--------------------------------------------------


    #--------------------------------------------------
    def Datum(self):
        return self.datum
    def Bemerkung(self):
        return self.bemerkung
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def VertretungsstundenListe():
        return Vertretungsstunde.Vertretungsstundenliste
    #--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Klasse:

    Klassenliste = []

    #--------------------------------------------------
        #create static method that can be called without object
        #method checks for already existing object and either returns the existing or creates a new one and returns this
    #--------------------------------------------------
    @staticmethod
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
            i.stundenliste = None
            i.stundenplan = None
            i.lehrerliste = None
            i.bezeichner = None
            del i
        Klasse.Klassenliste = []
    #--------------------------------------------------


    #--------------------------------------------------
    def __str__(self):
        return self.bezeichner
    def __eq__(self,other):
        return self.bezeichner==other.Bezeichner()
    def __lt__(self,other):
        b1 = self.bezeichner
        b2 = other.Bezeichner()

        # try:
        if b1[:2].isdigit():
            b1_z = int(b1[:2])
        # except:
        else:
            # try:
            if b1[:1].isdigit():
                b1_z = int(b1[:1])
            # except:
            else:
                b1_z = 20
        # try:
        if b2[:2].isdigit():
            b2_z = int(b2[:2])
        # except:
        else:
            # try:
            if b2[:1].isdigit():
                b2_z = int(b2[:1])
            # except:
            else:
                b2_z = 20

        if b1_z == b2_z:
            return b1 < b2
        else:
            return b1_z < b2_z
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

    #--------------------------------------------------
        #create static method that can be called without object
        #method checks for already existing object and either returns the existing or creates a new one and returns this
    #--------------------------------------------------
    @staticmethod
    def createRaum(bezeichner:str,stunde:Stunde):
        if bezeichner not in list(map(lambda c: c.bezeichner,Raum.Raumliste)):
            return Raum(bezeichner,stunde)
        else:
            for element in Raum.Raumliste:
                if element.bezeichner == bezeichner:
                    element.addStunde(stunde)
                    return element
    #--------------------------------------------------


    #--------------------------------------------------
    def __init__(self,bezeichner:str,stunde:Stunde):
        self.bezeichner = bezeichner

        self.stundenliste = []
        self.stundenplan = [[],[],[],[],[]]
        self.blockiert = []

        Raum.Raumliste.append(self)
        self.addStunde(stunde)
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Raum.Raumliste:
            i.bezeichner = None
            i.stundenliste = None
            i.stundenplan = None
            del i
        Raum.Raumliste = []
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
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)
    def addBlockiert(self,datum,von:int,bis:int): #(self,datum:Tag,von:int,bis:int)
        self.blockiert.append(Blockierung(self,datum,von,bis))
    #--------------------------------------------------


    #--------------------------------------------------
    def Bezeichner(self):
        return self.bezeichner
    def Stundenplan(self):
        return self.stundenplan
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def RaumListe():
        return Raum.Raumliste
    #--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Lehrer:

    Lehrerliste = []

    #--------------------------------------------------
        #create static method that can be called without object
        #method checks for already existing object and either returns the existing or creates a new one and returns this
    #--------------------------------------------------
    @staticmethod
    def createLehrer(bezeichner:str,stunde:Stunde):
        if bezeichner not in list(map(lambda c: c.bezeichner,Lehrer.Lehrerliste)):
            return Lehrer(bezeichner,stunde)
        else:
            for element in Lehrer.Lehrerliste:
                if element.bezeichner == bezeichner:
                    element.addStunde(stunde)
                    return element
    #--------------------------------------------------


    #--------------------------------------------------
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


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Lehrer.Lehrerliste:
            i.bezeichner = None
            i.stundenliste = None
            i.stundenplan = None
            i.absolvierteVertretungen = None
            i.faecherliste = None
            i.blockiert = None
            del i
        Lehrer.Lehrerliste = []
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
        self.stundenplan = Tools.sortStundenliste(self.stundenliste)
        # automatically add fach to faecherliste if not already in it
        if stunde.Fach() not in self.faecherliste:
            self.faecherliste.append(stunde.Fach())

    def addBlockiert(self,datum,von:int,bis:int): #(self,datum:Tag,von:int,bis:int)
        self.blockiert.append(Blockierung(self,datum,von,bis))
        self.blockiert.sort()
    def Blockiert(self):
        return self.blockiert
    #--------------------------------------------------


    #--------------------------------------------------
    def Bezeichner(self):
        return self.bezeichner
    def Stundenliste(self):
        return self.stundenliste
    def Stundenplan(self):
        return self.stundenplan
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def LehrerListe():
        return Lehrer.Lehrerliste
    #--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Fach:

    Fachliste = []

    #--------------------------------------------------
        #create static method that can be called without object
        #method checks for already existing object and either returns the existing or creates a new one and returns this
    #--------------------------------------------------
    @staticmethod
    def createFach(bezeichner:str):
        if bezeichner not in list(map(lambda c: c.bezeichner,Fach.Fachliste)):
            return Fach(bezeichner)
        else:
            for element in Fach.Fachliste:
                if element.bezeichner == bezeichner:
                    return element
    #--------------------------------------------------


    #--------------------------------------------------
    def __init__(self,bezeichner:str):
        self.bezeichner = bezeichner
        Fach.Fachliste.append(self)
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Fach.Fachliste:
            i.bezeichner = None
            del i
        Fach.Fachliste = []
    #--------------------------------------------------


    #--------------------------------------------------
    def __str__(self):
        return self.bezeichner
    def __eq__(self,other):
        return self.bezeichner == other.Bezeichner()
    def __lt__(self,other):
        return self.bezeichner < other.Bezeichner()
    #--------------------------------------------------


    #--------------------------------------------------
    def Bezeichner(self):
        return self.bezeichner
    #--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------


#--------------------------------------------------
#--------------------------------------------------
class Tag(QDate):

    tagListe = []

    #--------------------------------------------------
        #create static method that can be called without object
        # method checks for already existing object and either returns the existing or creates a new one and returns this
    #--------------------------------------------------
    @staticmethod
    def createTag(qdate:QDate):
        if qdate not in Tag.tagListe:
            return Tag(qdate)
        else:
            for element in Tag.tagListe:
                if element == qdate:
                    return element
    #--------------------------------------------------


    #--------------------------------------------------
    def __init__(self,qdate:QDate):
        super().__init__(qdate)
        self.blockierteLehrer = []
        self.blockierteRaeume = []
        self.ersatzstunden = []
        Tag.tagListe.append(self)
        self.informationen = ""


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


    #--------------------------------------------------
    @staticmethod
    def clearData():
        for i in Tag.tagListe:
            i.informationen = None
            i.blockierteLehrer = None
            i.blockierteRaeume = None
            i.ersatzstunden = None
            i.stunden = None
            del i
        Tag.tagListe = []
    #--------------------------------------------------


    #--------------------------------------------------
    def __eq__(self,other):
        return self.getDate() == other.getDate()
    def __lt__(self,other):
        return self.getDate() < other.getDate()
    def __str__(self):
        s = str(self.getDate())
        s = s[1:len(s)-1]
        return s
    #--------------------------------------------------


    #--------------------------------------------------
    def addBlockierterLehrer(self,lehrer): #(self,lehrer:Blockierung)
        if lehrer not in self.blockierteLehrer:
            # auf alte Blockierung pruefen, um Doppelung zu vermeiden
            self.blockierteLehrer.append(lehrer)
    def addBlockierterRaum(self,raum): #(self,raum:Blockierung)
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
    def addInformationen(self,info:str):
        if self.informationen != "":
            self.informationen += "\n"
        self.informationen += info
    #--------------------------------------------------


    #--------------------------------------------------
    def BlockierteLehrer(self):
        return self.blockierteLehrer
    def BlockierteRaeume(self):
        return self.blockierteRaeume
    def Ersatzstunden(self):
        return self.ersatzstunden
    def Stunden(self):
        return self.stunden
    def Informationen(self):
        return self.informationen
    #--------------------------------------------------


    #--------------------------------------------------
    def setInformationen(self,info:str):
        self.informationen = info
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def TagListe():
        return Tag.tagListe
    #--------------------------------------------------
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
            self.datum.addBlockierterLehrer(self)
            Blockierung.blockierteLehrer.append(self)
        elif isinstance(self.blockiertesObjekt,Raum):
            self.datum.addBlockierterRaum(self)
            Blockierung.blockierteRaeume.append(self)
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def clearData():
        Blockierung.blockierteLehrer = []
        Blockierung.blockierteRaeume = []
    #--------------------------------------------------


    #--------------------------------------------------
    def __str__(self):
        bO = str(self.blockiertesObjekt)
        d = str(self.datum)
        v = str(self.von)
        b = str(self.bis)
        return bO + ";" + d + ";" + v + ";" + b
    def __eq__(self, other):
        return self.blockiertesObjekt == other.BlockiertesObjekt()
    def __lt__(self,other):
        return self.blockiertesObjekt < other.BlockiertesObjekt()
    #--------------------------------------------------


    #--------------------------------------------------
    def BlockiertesObjekt(self):
        return self.blockiertesObjekt
    def Datum(self):
        return self.datum
    def Von(self):
        return self.von
    def Bis(self):
        return self.bis
    #--------------------------------------------------


    #--------------------------------------------------
    @staticmethod
    def BlockierteLehrer():
        return Blockierung.blockierteLehrer
    @staticmethod
    def BlockierteRaeume():
        return Blockierung.blockierteRaeume
    #--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------