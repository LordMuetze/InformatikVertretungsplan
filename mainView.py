from PyQt5 import QtWidgets, uic
#from PyQt5.QtCore import QDate
from model import Vertretungsplan
from classes import Lehrer, Raum, Tag
#from classes import Stunde

class MainWindow:

    def __init__(self):

        #create main window
        self.app = QtWidgets.QApplication([])
        #self.mW = uic.loadUi("mainWindow.ui")
        self.mW = uic.loadUi("alternativeWindow.ui")




        #create model and set attribute
        #view calls model, not vice-versa! --> no self.view in model
        self.model = Vertretungsplan()
        self.datum = Tag.createTag(self.mW.de_mainDatum.date())


        #Connections
        #self.mainWindow.{Ausloeser}.{Aktion}.connect({MethodenAufruf})
        #Bsp.: self.mW.pushButton.clicked.connect(self.test)
        self.mW.actionSpeichern.triggered.connect(self.on_actionSpeichern_triggered)
        self.mW.action_ffnen.triggered.connect(self.on_action_ffnen_triggered)
        #self.mW.actionEinlesen.triggered.connect(self.on_actionEinlesen_triggered)
        self.mW.actionImportieren.triggered.connect(self.on_actionEinlesen_triggered)

        self.mW.de_mainDatum.dateChanged.connect(self.dateChanged)


        #launch GUI --> last step of __init__ because starts loop
        self.mW.show()
        self.app.exec()

    def on_actionSpeichern_triggered(self):
        self.mW.setEnabled(False)
        path = QtWidgets.QFileDialog.getSaveFileName(None,"Speichern unter","","CSV Files (*.csv);;All Files (*)")[0]
        if path != "":
            self.model.saveCSV(path)
            self.update()
        self.mW.setEnabled(True)


    def on_action_ffnen_triggered(self):
        self.mW.setEnabled(False)
        path = QtWidgets.QFileDialog().getOpenFileName(None,"Datei oeffnen","","CSV Files (*.csv);;All Files (*)")[0]
        if path != "":
            self.model.openCSV(path)
            self.update()
        self.mW.setEnabled(True)


    def on_actionEinlesen_triggered(self):
        self.mW.setEnabled(False)
        pathUnter = QtWidgets.QFileDialog().getOpenFileName(None,"Unter-Daei einlesen","","SPM Files (*.spm);;All Files (*)")[0]
        pathZuordnung = QtWidgets.QFileDialog().getOpenFileName(None,"Zuordnungs-Datei einlesen","","SPM Files (*.spm);;All Files (*)")[0]
        if pathUnter != "" and pathZuordnung != "":
            self.model.DateienEinlesen(pathUnter,pathZuordnung)
            self.update()
        self.mW.setEnabled(True)


    def dateChanged(self,date):
        self.datum = Tag.createTag(date)

    def update(self):

        # update QtableWidget tw_alleLehrer
        lehrerliste = Lehrer.LehrerListe()
        self.mW.tw_alleLehrer.setRowCount(len(lehrerliste))
        self.mW.tw_alleLehrer.setColumnCount(1)
        lehrerliste.sort()
        for i,item in enumerate(lehrerliste):
            self.mW.tw_alleLehrer.setItem(0,i, QtWidgets.QTableWidgetItem(str(item)))

        # update QtableWidget tw_alleRaeume
        raumliste = Raum.RaumListe()
        self.mW.tw_alleRaeume.setRowCount(len(raumliste))
        self.mW.tw_alleRaeume.setColumnCount(1)
        raumliste.sort()
        for i,item in enumerate(raumliste):
            self.mW.tw_alleRaeume.setItem(0,i, QtWidgets.QTableWidgetItem(str(item)))

        # update QtableWidget tw_abwesendeLehrer
        abwesendliste = self.datum.BlockierteLehrer()
        self.mW.tw_abwesendeLehrer.setRowCount(len(abwesendliste))
        self.mW.tw_abwesendeLehrer.setColumnCount(3)
        self.mW.tw_abwesendeLehrer.setHorizontalHeaderLabels(["Lehrer", "von Stunde", "bis einschl. Stunde"])
        abwesendliste.sort()
        for i,item in enumerate(abwesendliste):
            self.mW.tw_abwesendeLehrer.setItem(0,i, QtWidgets.QTableWidgetItem(str(item)))
            #von = filter(lambda c: c.datum==self.datum, item.Blockiert())[0]
            block = list(filter(lambda c: c.Datum()==self.datum,item.Blockiert()))[0]
            von = block.Von()
            bis = block.Bis()
            self.mW.tw_abwesendeLehrer.setItem(1,i, QtWidgets.QTableWidgetItem(str(von)))
            self.mW.tw_abwesendeLehrer.setItem(2,i, QtWidgets.QTableWidgetItem(str(bis)))

        # update QtableWidget tw_blockierteRaeume
        blockiertliste = self.datum.BlockierteRaeume()
        self.mW.tw_blockierteRaeume.setRowCount(len(blockiertliste))
        self.mW.tw_blockierteRaeume.setColumnCount(3)
        self.mW.tw_blockierteRaeume.setHorizontalHeaderLabels(["Raum", "von Stunde", "bis einschl. Stunde"])
        blockiertliste.sort()
        for i,item in enumerate(abwesendliste):
            self.mW.tw_blockierteRaeume.setItem(0,i, QtWidgets.QTableWidgetItem(str(item)))
            #von = filter(lambda c: c.datum==self.datum, item.Blockiert())[0]
            block = list(filter(lambda c: c.Datum()==self.datum,item.Blockiert()))[0]
            von = block.Von()
            bis = block.Bis()
            self.mW.tw_blockierteRaeume.setItem(1,i, QtWidgets.QTableWidgetItem(str(von)))
            self.mW.tw_blockierteRaeume.setItem(2,i, QtWidgets.QTableWidgetItem(str(bis)))
