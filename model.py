from classes import Stunde,Tag
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
    def vertretungErstellen(self,datum:Tag,stunde:Stunde,ersatzraum=0,ersatzlehrer=0):
        if ersatzraum != 0:
            raum = ersatzraum
        else:
            raum = stunde.Raum()

        if ersatzlehrer != 0:
            lehrer = ersatzlehrer
        else:
            lehrer = stunde.Lehrer()
        ersatzStunde = Stunde(stunde.Tag(),stunde.Stunde(),stunde.Klasse().Bezeichner(),lehrer.Bezeichner(),raum.Bezeichner(),stunde.Fach().Bezeichner(),ersatzstunde=True,datum=datum)
        datum.addErsatzstunde(ersatzStunde)



    def DateienEinlesen(self, pathUnter:str, pathZuordnung:str):
        dateiUnter = open(pathUnter, "r")
        stunden = dateiUnter.read().splitlines()
        dateiUnter.close()

        dateiZuordnung = open(pathZuordnung, "r")
        zuordnung = dateiZuordnung.read().splitlines()
        dateiZuordnung.close()

        while "" in stunden:
            stunden.remove("")

        stundenListen = [] #2d list
        for element in stunden:
            if element[0] == "U":
                a = element.split(" ")
                while "" in a:
                    a.remove("")
                if "//" in a: # if \\ in a
                    a = a[:a.index("//")]
                stundenListen.append(a)
        while [] in stundenListen:
            stundenListen.remove([])


        while "" in zuordnung:
            zuordnung.remove("")

        zuordnungListen = [] #2d list
        for element in zuordnung:
            if element[0] == "U":
                a = element.split(" ")
                while "" in a:
                    a.remove("")
                if "//" in a: # if \\ in a
                    a = a[:a.index("//")]
                zuordnungListen.append(a)
        while [] in zuordnungListen:
            zuordnungListen.remove([])

        
        dictionary = {} # ([unter],[zuord])
        for element in stundenListen:
            dictionary[element[0]] = element

        for element in zuordnungListen:
            dictionary[element[0]] = (dictionary[element[0]],element)

        for _, uz in dictionary.items():
            tag = Tools.convertWeekdayGerman(uz[0][1])
            stunde = uz[0][2]
            klasse = uz[1][1]
            lehrer = uz[0][5]
            raum = uz[0][3]
            fach = uz[1][2]

            Stunde(tag,stunde,klasse,lehrer,raum,fach)
        
        print("Import successful")

    
    # save all objects of Stunde to comma-separated csv
    def saveCSV(self,path):
        outputStandard = "Tag,Stunde,Klasse,Lehrer,Raum,Fach\n"
        outputVertretung = "Datum,Tag,Stunde,Klasse,Lehrer,Raum,Fach\n"

        stundenplan = Tools.sortStundenliste(Stunde.getStundenliste())
        for tag in stundenplan:
            for stunde in tag:
                if stunde.Ersatzstunde():
                    s = str(stunde.Datum()) + "," + str(stunde.Tag()) + "," + str(stunde.Stunde()) + "," + str(stunde.Klasse()) + "," + str(stunde.Lehrer()) + "," + str(stunde.Raum()) + "," + str(stunde.Fach()) + "\n"
                    outputVertretung += s
                else:
                    s = str(stunde.Tag()) + "," + str(stunde.Stunde()) + "," + str(stunde.Klasse()) + "," + str(stunde.Lehrer()) + "," + str(stunde.Raum()) + "," + str(stunde.Fach()) + "\n"
                    outputStandard += s

        
        file = open(path,"w")
        file.write("[Stundenplan]\n")
        file.write(outputStandard)
        file.write("[Vertretungen]\n")
        file.write(outputVertretung)
        file.close()
 
    def openCSV(self, path):
        file = open(path,"r")
        #content = file.readlines()
        content = file.read().splitlines() 

        # remove section-header [Stundenplan] & csv-header
        if content[0] == "[Stundenplan]":
            content.pop(0)
            content.pop(0)

        # read content until header [Vertretungen]
        while content[0] != "[Vertretungen]":
            line = content.pop(0).split(",")
            #line[len(line)-1].replace("\n","")
            Stunde(int(line[0]),int(line[1]),line[2],line[3],line[4],line[5])

        # remove section-header [Vertretungen] & csv-header
        if content[0] == "[Vertretungen]":
            content.pop(0)
            content.pop(0)
        
        # read content until file's empty
        while len(content) > 0:
            line = content.pop(0).split(",")
            Stunde(int(line[1]),int(line[2]),line[3],line[4],line[5],line[6],ersatzstunde=True,datum=line[0])

        for i in Stunde.Stundenliste:
            print(i)