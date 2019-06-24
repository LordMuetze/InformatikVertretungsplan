from classes import *
from tools import Tools

class Vertretungsplan:
    #--------------------------------------------------
    def vertretungErstellen(self,datum:Tag,stunde:Stunde,ersatzraum=0,ersatzlehrer=0):
        if ersatzraum != 0:
            raum = ersatzraum
        else:
            raum = str(stunde.Raum())

        if ersatzlehrer != 0:
            lehrer = ersatzlehrer
        else:
            lehrer = str(stunde.Lehrer())

        tag = stunde.Tag()
        unterrichtsstunde = stunde.Stunde()
        klasse = str(stunde.Klasse())
        fach = str(stunde.Fach())

        ersatzStunde = Stunde(tag,unterrichtsstunde,klasse,lehrer,raum,fach,ersatzstunde=True,datum=datum)
        datum.addErsatzstunde(ersatzStunde)
    #--------------------------------------------------


    #--------------------------------------------------
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
    #--------------------------------------------------


    #--------------------------------------------------
        # save all objects of Stunde to ;-separated csv
    #--------------------------------------------------
    def saveCSV(self,path):
        outputStandard = "Tag;Stunde;Klasse;Lehrer;Raum;Fach\n"
        outputVertretung = "Datum;Tag;Stunde;Klasse;Lehrer;Raum;Fach\n"
        outputAbwesend = "Bezeichner;Datum;von;bis\n"
        outputBlockiert = "Bezeichner;Datum;von;bis\n"

        stundenplan = Tools.sortStundenliste(Stunde.getStundenliste())
        for tag in stundenplan:
            for stunde in tag:
                if stunde.Ersatzstunde():
                    s = str(stunde.Datum()) + ";" + str(stunde.Tag()) + ";" + str(stunde.Stunde()) + ";" + str(stunde.Klasse()) + ";" + str(stunde.Lehrer()) + ";" + str(stunde.Raum()) + ";" + str(stunde.Fach()) + "\n"
                    outputVertretung += s
                else:
                    s = str(stunde.Tag()) + ";" + str(stunde.Stunde()) + ";" + str(stunde.Klasse()) + ";" + str(stunde.Lehrer()) + ";" + str(stunde.Raum()) + ";" + str(stunde.Fach()) + "\n"
                    outputStandard += s

        for block in Blockierung.BlockierteLehrer():
            s = str(block) + "\n"
            outputAbwesend += s

        for block in Blockierung.BlockierteRaeume():
            s = str(block) + "\n"
            outputBlockiert += s


        file = open(path,"w")
        file.write("[Stundenplan]\n")
        file.write(outputStandard)
        file.write("[Vertretungen]\n")
        file.write(outputVertretung)
        file.write("[Abwesend]\n")
        file.write(outputAbwesend)
        file.write("[Blockiert]\n")
        file.write(outputBlockiert)
        file.close()

        file = open("config/config.ini","w")
        file.write(path)
        file.close()
    #--------------------------------------------------


    #--------------------------------------------------
    def openCSV(self, path):
        file = open(path,"r")
        content = file.read().splitlines()
        file.close()
        # remove section-header [Stundenplan] & csv-header
        if content[0] == "[Stundenplan]":
            content.pop(0)
            content.pop(0)
        # read content of [Stundenplan] until header [Vertretungen]
        while content[0] != "[Vertretungen]":
            line = content.pop(0).split(";")
            Stunde(int(line[0]),int(line[1]),line[2],line[3],line[4],line[5])


        # remove section-header [Vertretungen] & csv-header
        if content[0] == "[Vertretungen]":
            content.pop(0)
            content.pop(0)
        # read content of [Vertretungen] until header [Abwesend]
        while content[0] != "[Abwesend]":
            line = content.pop(0).split(";")
            Stunde(int(line[1]),int(line[2]),line[3],line[4],line[5],line[6],ersatzstunde=True,datum=line[0])


        # remove section-header [Abwesend] & csv-header
        if content[0] == "[Abwesend]":
            content.pop(0)
            content.pop(0)
        # read content of [Abwesend] until header [Blockiert]
        while content[0] != "[Blockiert]":
            line = content.pop(0).split(";")
            leh = line[0]
            ds = line[1]
            dl = ds.split(",")
            datum = Tag.createTag(QDate(int(dl[0]),int(dl[1]),int(dl[2])))
            ab = int(line[2])
            bis = int(line[3])
            lehrer = list(filter(lambda c: str(c)==leh,Lehrer.LehrerListe()))[0]
            tag = Tag.createTag(datum)
            Blockierung(lehrer,tag,ab,bis)


        # remove section-header [Blockiert] & csv-header
        if content[0] == "[Blockiert]":
            content.pop(0)
            content.pop(0)
        # read content of [Blockiert] until file's empty
        while content:
            line = content.pop(0).split(";")
        file = open("config/config.ini","w")
        file.write(path)
        file.close()
    #--------------------------------------------------


    #--------------------------------------------------
    def clearData(self):
        Stunde.clearData()
        Klasse.clearData()
        Raum.clearData()
        Lehrer.clearData()
        Fach.clearData()
        Tag.clearData()
        Blockierung.clearData()
    #--------------------------------------------------