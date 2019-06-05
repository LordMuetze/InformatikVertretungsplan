from classes import *
from tools import Tools

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

    def DateienEinlesen(self, pathUnter:str, pathZuordnung:str):
        dateiUnter = open(pathUnter, "r")
        dateiZuordnung = open(pathZuordnung, "r")
        stunden = dateiUnter.readlines()
        zuordnung = dateiZuordnung.readlines()
        
        stundenListen = []
        for element in stunden:
            a = element.split(" ")
            while "" in a:
                a.remove("")
            stundenListen.append(a)

        zuordnungListen = []
        for element in zuordnung:
            a = element.split(" ")
            while "" in a:
                a.remove("")
            zuordnungListen.append(a)

        dateiZuordnung.close()
        dateiUnter.close()

    
    # save all objects of Stunde to comma-separated csv
    def saveCSV(self,path):
        outputStandard = "Tag,Stunde,Klasse,Lehrer,Raum,Fach\n"
        outputVertretung = "Datum,Tag,Stunde,Klasse,Lehrer,Raum,Fach\n"

        stundenplan = Tools.sortStundenliste(Stunde.getStundenliste())
        for tag in stundenplan:
            for stunde in tag:
                if stunde.Ersatzstunde():
                    s = stunde.Tag() + stunde.Stunde() + stunde.Klasse() + stunde.Lehrer() + stunde.Raum() + stunde.Fach() + "\n"
                    outputVertretung += s
                else:
                    s = stunde.Tag() + stunde.Stunde() + stunde.Klasse() + stunde.Lehrer() + stunde.Raum() + stunde.Fach() + "\n"
                    outputStandard += s
        
        file = open(path,"w")
        file.write("[Stundenplan]\n")
        file.write(outputStandard)
        file.write("[Vertretungen]\n")
        file.write(outputVertretung)
        file.close()
        
 
    def openCSV(self, path):
        pass