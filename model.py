from PyQt5.QtCore import QDate
from fpdf import FPDF
from classes import Stunde,Vertretungsstunde,Klasse,Lehrer,Raum,Fach,Tag,Blockierung
from tools import Tools


class Vertretungsplan:
    #--------------------------------------------------
    def vertretungErstellen(self,datum:Tag,stunde:Stunde,bemerkung,ersatzraum=0,ersatzlehrer=0):
        if ersatzraum != 0:
            raum = ersatzraum
            if ersatzraum != "":
                bemerkung = "Raumtausch; " + "\n" + bemerkung
        else:
            raum = str(stunde.Raum())

        if ersatzlehrer != 0:
            lehrer = ersatzlehrer
        else:
            lehrer = str(stunde.Lehrer())

        # check if lehrer or raum have value for Entfall and set other one to it
        if ersatzraum == "":
            lehrer = "Entfall"
        if ersatzlehrer == "Entfall":
            raum = ""

        tag = stunde.Tag()
        unterrichtsstunde = stunde.Stunde()
        klasse = str(stunde.Klasse())
        fach = str(stunde.Fach())

        Vertretungsstunde(tag,unterrichtsstunde,klasse,lehrer,raum,fach,datum,bemerkung)
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
        # replace csv-triggers (";", "\n") in strings by "," & "\t" to prevent wrong formatting
    #--------------------------------------------------
    def saveCSV(self,path):
        separator = ";"
        outputStandard = "Tag;Stunde;Klasse;Lehrer;Raum;Fach\n"
        outputVertretung = "Datum;Tag;Stunde;Klasse;Lehrer;Raum;Fach\n"
        outputAbwesend = "Bezeichner;Datum;von;bis\n"
        outputBlockiert = "Bezeichner;Datum;von;bis\n"
        outputInfo = "Datum;Information\n"

        stundenplan = Tools.sortStundenliste(Stunde.StundenListe())
        for tag in stundenplan:
            for stunde in tag:
                s = (str(stunde.Tag()).replace(";",",").replace("\n","\t") + separator +
                     str(stunde.Stunde()).replace(";",",").replace("\n","\t") + separator +
                     str(stunde.Klasse()).replace(";",",").replace("\n","\t") + separator +
                     str(stunde.Lehrer()).replace(";",",").replace("\n","\t") + separator +
                     str(stunde.Raum()).replace(";",",").replace("\n","\t") + separator +
                     str(stunde.Fach()).replace(";",",").replace("\n","\t") + "\n")
                outputStandard += s

        for stunde in Vertretungsstunde.VertretungsstundenListe():
            s = (str(stunde.Datum()) + separator +
                 str(stunde.Tag()).replace(";",",").replace("\n","\t") + separator +
                 str(stunde.Stunde()).replace(";",",").replace("\n","\t") + separator +
                 str(stunde.Klasse()).replace(";",",").replace("\n","\t") + separator +
                 str(stunde.Lehrer()).replace(";",",").replace("\n","\t") + separator +
                 str(stunde.Raum()).replace(";",",").replace("\n","\t") + separator +
                 str(stunde.Fach()).replace(";",",").replace("\n","\t") + separator +
                 stunde.Bemerkung().replace(";",",").replace("\n","\t") + "\n")
            outputVertretung += s

        for block in Blockierung.BlockierteLehrer():
            s = str(block).replace("\n","\t") + "\n"
            outputAbwesend += s

        for block in Blockierung.BlockierteRaeume():
            s = str(block).replace("\n","\t") + "\n"
            outputBlockiert += s

        l = list(filter(lambda c: c.Informationen()!="",Tag.TagListe()))
        for tag in l:
            s = (str(tag) + separator +
                 tag.Informationen().replace(";",",").replace("\n","\t") + "\n")
            outputInfo += s


        file = open(path,"w")
        file.write("[Stundenplan]\n")
        file.write(outputStandard)
        file.write("[Vertretungen]\n")
        file.write(outputVertretung)
        file.write("[Abwesend]\n")
        file.write(outputAbwesend)
        file.write("[Blockiert]\n")
        file.write(outputBlockiert)
        file.write("[Informationen]\n")
        file.write(outputInfo)
        file.close()

        file = open("config/config.ini","w")
        file.write(path)
        file.close()
    #--------------------------------------------------


    #--------------------------------------------------
    def openCSV(self, path):
        separator = ";"
        file = open(path,"r")
        content = file.read().splitlines()
        file.close()

        # remove empty lines
        while "" in content:
            content.remove("")

        # remove section-header [Stundenplan] & csv-header
        if content[0] == "[Stundenplan]":
            content.pop(0)
            content.pop(0)
            # read content of [Stundenplan] until header [Vertretungen]
            while content[0] != "[Vertretungen]":
                line = content.pop(0).split(separator)
                Stunde(int(line[0]),int(line[1]),line[2],line[3],line[4],line[5])


        # remove section-header [Vertretungen] & csv-header
        if content[0] == "[Vertretungen]":
            content.pop(0)
            content.pop(0)
            # read content of [Vertretungen] until header [Abwesend]
            while content[0] != "[Abwesend]":
                line = content.pop(0).split(separator)
                datumL = line[0].split(", ")
                datum = Tag.createTag(QDate(int(datumL[0]),int(datumL[1]),int(datumL[2])))
                Vertretungsstunde(int(line[1]),int(line[2]),line[3],line[4],line[5],line[6],datum,line[7])


        # remove section-header [Abwesend] & csv-header
        if content[0] == "[Abwesend]":
            content.pop(0)
            content.pop(0)
            # read content of [Abwesend] until header [Blockiert]
            while content[0] != "[Blockiert]":
                line = content.pop(0).split(separator)
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
            # read content of [Blockiert] until header [Informationen]
            while content[0] != "[Informationen]":
                line = content.pop(0).split(separator)
                rau = line[0]
                ds = line[1]
                dl = ds.split(",")
                datum = Tag.createTag(QDate(int(dl[0]),int(dl[1]),int(dl[2])))
                ab = int(line[2])
                bis = int(line[3])
                raum = list(filter(lambda c: str(c)==rau,Raum.RaumListe()))[0]
                tag = Tag.createTag(datum)
                Blockierung(raum,tag,ab,bis)


        # remove section-header [Informationen] & csv-header
        if content[0] == "[Informationen]":
            content.pop(0)
            content.pop(0)
            # read content of [Blockiert] until file's empty
            while content:
                line = content.pop(0).split(separator)
                dl = line[0].split(",")
                datum = Tag.createTag(QDate(int(dl[0]),int(dl[1]),int(dl[2])))
                datum.addInformationen(line[1].replace("\t","\n"))


        file = open("config/config.ini","w")
        file.write(path)
        file.close()
    #--------------------------------------------------


    #--------------------------------------------------
    def exportierenPDF(self, path, datum):
        font = "Helvetica"

        # basic pdf setup
        #----------------------------------------
        pdf = FPDF()
        pdf.set_font(font, size=12)
        pdf.add_page()
        row_height = pdf.font_size*1.5
        #----------------------------------------


        # set title
        #----------------------------------------
        datumStr = str(Tools.convertWeekdayGerman(datum.dayOfWeek())) + ', ' + str(datum.day()) + '.' + str(datum.month()) + '.' + str(datum.year())
        title = "Vertretungsplan von " + datumStr
        pdf.set_font(font, 'B', 14)
        w = pdf.get_string_width(title) + 6
        pdf.set_x((210 - w) / 2)
        pdf.cell(w, 9, txt=title, border=0)
        pdf.ln(10)
        #----------------------------------------

        if datum.Informationen() != "":
            # set info title
            #----------------------------------------
            title = "allgemeine Informationen"
            pdf.set_font(font, '', 12)
            w = pdf.get_string_width(title) + 6
            pdf.set_x(10)
            pdf.cell(w, 9, txt=title, border=0)
            pdf.ln(10)
            #----------------------------------------


            # set info
            #----------------------------------------
            pdf.set_font(font, 'I', 11)
            w = pdf.get_string_width(datum.Informationen()) + 6
            pdf.set_x(10)
            pdf.cell(w, 9, txt=datum.Informationen(), border=1)
            pdf.ln(10)
            pdf.ln(10)
            #----------------------------------------


        # set table
        #----------------------------------------
        # content = [((("str",width),("str",width),("str",width),("str",width),("str",width)),("Art","typ",size)),
        #            ((("str",width),("str",width),("str",width),("str",width),("str",width)),("Art","typ",size))]
        content = []
        t1 = ("Klasse",pdf.get_string_width("Klasse") + 6)
        t2 = ("Std",pdf.get_string_width("Std") + 6)
        t3 = ("Fach",pdf.get_string_width("Fach") + 6)
        t4 = ("Vertretung",pdf.get_string_width("Vertretung") + 6)
        t5 = ("Raum",pdf.get_string_width("Raum") + 6)
        t6 = ("Bemerkung",pdf.w - t1[1] - t2[1] - t3[1] - t4[1] - t5[1] - 20)
        content.append(((t1,t2,t3,t4,t5,t6),(font, 'B', 13)))
        for stunde in Vertretungsstunde.VertretungsstundenListe():
            if stunde.datum == datum:
                klasse = (str(stunde.Klasse()),t1[1])
                stu = (str(stunde.Stunde()),t2[1])
                fach = (str(stunde.Fach()),t3[1])
                lehrer = (str(stunde.Lehrer()),t4[1])
                raum = (str(stunde.Raum()),t5[1])
                bemerkung = (stunde.Bemerkung(),t6[1])
                item = (klasse,stu,fach,lehrer,raum,bemerkung)
                content.append((item,(font, '', 12)))

        for row in content:
            font = row[1][0]
            style = row[1][1]
            size = row[1][2]
            pdf.set_font(font,style,size)
            row_height = pdf.font_size*1.5
            for item in row[0]:
                pdf.cell(item[1], row_height,txt=item[0], border=1)
            pdf.ln(row_height)
        #----------------------------------------

        pdf.output(path)
    #--------------------------------------------------


    #--------------------------------------------------
    def clearData(self):
        for i in range(2): # clear data twice to make sure every reference to any object is deleted
            Stunde.clearData()
            Klasse.clearData()
            Raum.clearData()
            Lehrer.clearData()
            Fach.clearData()
            Tag.clearData()
            Blockierung.clearData()
    #--------------------------------------------------