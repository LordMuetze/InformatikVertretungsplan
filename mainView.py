from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
from model import Vertretungsplan
from classes import Lehrer,Raum,Tag,Blockierung

class MainWindow:


    #--------------------------------------------------
    def __init__(self):

        #create main window
        self.app = QtWidgets.QApplication([])
        #self.mW = uic.loadUi("mainWindow.ui")
        self.mW = uic.loadUi("alternativeWindow.ui")
        self.dialog = None


        #create model and set attribute
        #view calls model, not vice-versa! --> no self.view in model
        self.model = Vertretungsplan()

        #set datum to dateEdit
        self.datum = Tag.createTag(self.mW.de_mainDatum.date())


        #Connections
        #QtCore.QMetaObject.connectSlotsByName(self.mW)
        #self.mainWindow.{Ausloeser}.{Aktion}.connect({MethodenAufruf})
        self.mW.actionSpeichern.triggered.connect(self.on_actionSpeichern_triggered)
        self.mW.action_ffnen.triggered.connect(self.on_action_ffnen_triggered)
        self.mW.actionImportieren.triggered.connect(self.on_actionImportieren_triggered)
        self.mW.actionAbwesenheit_eintragen.triggered.connect(self.on_actionAbwesenheit_eintragen_triggered)
        self.mW.actionRaum_blockieren.triggered.connect(self.on_actionRaum_blockieren_eintragen_triggered)
        self.mW.actionallgemeiner_Unterrichtsschluss.triggered.connect(self.on_actionallgemeiner_Unterrichtsschluss_eintragen_triggered)
        self.mW.btn_datumHeute.clicked.connect(self.on_btn_datumHeute_clicked)
        self.mW.de_mainDatum.dateChanged.connect(self.on_de_mainDatum_dateChanged)


        self.mW.show()
        #open last file
        try:
            file = open("config.ini","r")
            path = file.readline()
            self.model.openCSV(path)
            file.close()
        except:
            pass
        self.update()

        #launch GUI --> last step of __init__ because starts loop
        self.app.exec()
    #--------------------------------------------------


    #--------------------------------------------------
    def on_btn_datumHeute_clicked(self):
        self.mW.de_mainDatum.setDate(QDate.currentDate())
    #--------------------------------------------------


    #--------------------------------------------------
    def on_actionSpeichern_triggered(self):
        self.mW.setEnabled(False)
        path = QtWidgets.QFileDialog.getSaveFileName(None,"Speichern unter","","CSV Files (*.csv);;All Files (*)")[0]
        if path != "":
            self.model.saveCSV(path)
            self.update()
        self.mW.setEnabled(True)
    #--------------------------------------------------


    #--------------------------------------------------
    def on_action_ffnen_triggered(self):
        self.mW.setEnabled(False)
        path = QtWidgets.QFileDialog().getOpenFileName(None,"Datei oeffnen","","CSV Files (*.csv);;All Files (*)")[0]
        if path != "":
            self.model.openCSV(path)
            self.update()
        self.mW.setEnabled(True)
    #--------------------------------------------------


    #--------------------------------------------------
    def on_actionImportieren_triggered(self):
        self.mW.setEnabled(False)
        pathUnter = QtWidgets.QFileDialog().getOpenFileName(None,"Unter-Daei einlesen","","SPM Files (*.spm);;All Files (*)")[0]
        pathZuordnung = QtWidgets.QFileDialog().getOpenFileName(None,"Zuordnungs-Datei einlesen","","SPM Files (*.spm);;All Files (*)")[0]
        if pathUnter != "" and pathZuordnung != "":
            self.model.DateienEinlesen(pathUnter,pathZuordnung)
            self.update()
        self.mW.setEnabled(True)
    #--------------------------------------------------


    #--------------------------------------------------
    def on_actionAbwesenheit_eintragen_triggered(self):
        print("Works")
    #--------------------------------------------------


    #--------------------------------------------------
    def on_actionRaum_blockieren_eintragen_triggered(self):
        print("Works")
    #--------------------------------------------------


    #--------------------------------------------------
    def on_actionallgemeiner_Unterrichtsschluss_eintragen_triggered(self):
        self.dialog = uic.loadUi("DialogUnterrichtsschluss.ui")
        self.dialog.btn_eintragen.clicked.connect(self.on_btn_eintragen_clicked)
        self.dialog.calendarWidget.setSelectedDate(self.mW.de_mainDatum.date())
        self.dialog.show()
    #--------------------------------------------------


    #--------------------------------------------------
    def on_btn_eintragen_clicked(self):
        datum = self.dialog.calendarWidget.selectedDate()
        ab = self.dialog.sb_abStunde.value()
        tag = Tag.createTag(datum)
        stunden = list(filter(lambda c: c.Stunde() >= ab,tag.Stunden()))
        for s in stunden:
            lehrer = "Entfall"
            raum = ""
            self.model.vertretungErstellen(tag,s,ersatzlehrer=lehrer,ersatzraum=raum)
        self.dialog.done(0)
        self.update()
    #--------------------------------------------------


    #--------------------------------------------------
    def on_de_mainDatum_dateChanged(self,date):
        self.datum = Tag.createTag(date)
        self.update()
    #--------------------------------------------------


    #--------------------------------------------------
    def update(self):
        self.mW.setEnabled(False)
        # update QtableWidget tw_alleLehrer
        lehrerliste = Lehrer.LehrerListe()
        self.mW.tw_alleLehrer.setRowCount(len(lehrerliste))
        self.mW.tw_alleLehrer.setColumnCount(1)
        lehrerliste.sort()
        for i,item in enumerate(lehrerliste):
            self.mW.tw_alleLehrer.setItem(i,0, QtWidgets.QTableWidgetItem(str(item)))


        # update QtableWidget tw_alleRaeume
        raumliste = Raum.RaumListe()
        self.mW.tw_alleRaeume.setRowCount(len(raumliste))
        self.mW.tw_alleRaeume.setColumnCount(1)
        raumliste.sort()
        for i,item in enumerate(raumliste):
            self.mW.tw_alleRaeume.setItem(i,0, QtWidgets.QTableWidgetItem(str(item)))


        # update QtableWidget tw_abwesendeLehrer
        abwesendliste = list(filter(lambda c: c.Datum()==self.datum,Blockierung.BlockierteLehrer())) # blockierte Lehrer für diesen Tag filtern
        abwesendliste.sort() #Lehrer alphabetisch sortieren

        self.mW.tw_abwesendeLehrer.setRowCount(len(abwesendliste))
        self.mW.tw_abwesendeLehrer.setColumnCount(3)
        self.mW.tw_abwesendeLehrer.setHorizontalHeaderLabels(["Lehrer", "von Stunde", "bis einschl. Stunde"])

        for i,item in enumerate(abwesendliste):
            von = item.Von()
            bis = item.Bis()
            lehrer = item.BlockiertesObjekt()
            self.mW.tw_abwesendeLehrer.setItem(i,0, QtWidgets.QTableWidgetItem(str(lehrer)))
            self.mW.tw_abwesendeLehrer.setItem(i,1, QtWidgets.QTableWidgetItem(str(von)))
            self.mW.tw_abwesendeLehrer.setItem(i,2, QtWidgets.QTableWidgetItem(str(bis)))


        # update QtableWidget tw_blockierteRaeume
        blockiertliste = list(filter(lambda c: c.Datum()==self.datum,Blockierung.BlockierteRaeume())) # blockierte Raeume für diesen Tag filtern
        blockiertliste.sort() #Raeume alphabetisch sortieren

        self.mW.tw_blockierteRaeume.setRowCount(len(blockiertliste))
        self.mW.tw_blockierteRaeume.setColumnCount(3)
        self.mW.tw_blockierteRaeume.setHorizontalHeaderLabels(["Raum", "von Stunde", "bis einschl. Stunde"])

        for i,item in enumerate(blockiertliste):
            von = item.Von()
            bis = item.Bis()
            raum = item.BlockiertesObjekt()
            self.mW.tw_blockierteRaeume.setItem(i,0, QtWidgets.QTableWidgetItem(str(raum)))
            self.mW.tw_blockierteRaeume.setItem(i,1, QtWidgets.QTableWidgetItem(str(von)))
            self.mW.tw_blockierteRaeume.setItem(i,2, QtWidgets.QTableWidgetItem(str(bis)))


        # update QtableWidget tw_vertretungsstunden
        vertretungsliste = self.datum.Ersatzstunden()
        self.mW.tw_vertretungsstunden.setRowCount(len(vertretungsliste))
        self.mW.tw_vertretungsstunden.setColumnCount(4)
        self.mW.tw_vertretungsstunden.setHorizontalHeaderLabels(["Klasse","Stunde","Fach","Vertretung","Raum"])
        vertretungsliste.sort()
        for i,item in enumerate(vertretungsliste):
            klasse = item.Klasse()
            stunde = item.Stunde()
            lehrer = item.Lehrer()
            raum = item.Raum()
            fach = item.Fach()
            self.mW.tw_vertretungsstunden.setItem(i,0, QtWidgets.QTableWidgetItem(str(klasse)))
            self.mW.tw_vertretungsstunden.setItem(i,1, QtWidgets.QTableWidgetItem(str(stunde)))
            self.mW.tw_vertretungsstunden.setItem(i,2, QtWidgets.QTableWidgetItem(str(fach)))
            self.mW.tw_vertretungsstunden.setItem(i,3, QtWidgets.QTableWidgetItem(str(lehrer)))
            self.mW.tw_vertretungsstunden.setItem(i,4, QtWidgets.QTableWidgetItem(str(raum)))

        self.mW.setEnabled(True)
    #--------------------------------------------------