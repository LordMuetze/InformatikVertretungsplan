from classes import *

class Vertretungsplan:


    def __init__(self):
        pass

    def addStunde(self, daten:str):
        pass

    def freieLehrer(self):
        pass

    def freieRaeume(self):
        pass

    def lehrerBlockieren(self,lehrer):
        pass

    def raumBlockieren(self,raum):
        pass

    def lehrerWarnungen(self):
        pass

    def raumWarnungen(self):
        pass

    def unterrichtsschlussErstellen(self):
        pass

    #--------------------------------------------------
        # aufrufen als (0,0 ist Montag erste Stunde):
        # vertretungErstellen(0,0,ersatzraum=xy)
        # vertretungErstellen(0,0,ersatzlehrer=xy)
    #--------------------------------------------------
    def vertretungErstellen(self,tag:Tag,stunde:Stunde,ersatzraum=0,ersatzlehrer=0):
        if ersatzraum != 0:
            raum = ersatzraum
        else:
            raum = stunde.Raum()

        if ersatzlehrer != 0:
            lehrer = ersatzlehrer
        else:
            lehrer = stunde.Lehrer()
        ersatzStunde = Stunde(stunde.Klasse(),raum,lehrer,stunde.Fach(),stunde.Tag(),stunde.Stunde(),ersatzstunde=True)
        tag.addErsatzstunde(ersatzStunde)