from PyQt5 import QtWidgets, uic
from model import Vertretungsplan
#from classes import Stunde
import sys

class MainWindow:

    def __init__(self):

        #create main window
        self.app = QtWidgets.QApplication([])
        #self.mW = uic.loadUi("mainWindow.ui")
        self.mW = uic.loadUi("alternativeWindow.ui")

    
        #create model and set attribute
        #view calls model, not vice-versa! --> no self.view in model
        self.model = Vertretungsplan()

        #self.mW.


        #Connections
        #self.mainWindow.{Ausloeser}.{Aktion}.connect({MethodenAufruf})
        #Bsp.: self.mW.pushButton.clicked.connect(self.test)
        self.mW.actionSpeichern.triggered.connect(self.on_actionSpeichern_triggered)
        self.mW.action_ffnen.triggered.connect(self.on_action_ffnen_triggered)
        #self.mW.actionEinlesen.triggered.connect(self.on_actionEinlesen_triggered)
        self.mW.actionImportieren.triggered.connect(self.on_actionEinlesen_triggered)

        #launch GUI --> last step of __init__ because starts loop
        self.mW.show()
        self.app.exec()
    
    def on_actionSpeichern_triggered(self):
        path = QtWidgets.QFileDialog.getSaveFileName(None,"Speichern unter","","CSV Files (*.csv);;All Files (*)")[0]
        #path = 'C:/Users/Admin/Desktop/Vertretungsplan/InformatikVertretungsplan/Testdateien/CSVExports/test1.csv'
        self.model.saveCSV(path)
        self.update()
    
    def on_action_ffnen_triggered(self):
        path = QtWidgets.QFileDialog().getOpenFileName(None,"Datei oeffnen","","CSV Files (*.csv);;All Files (*)")[0]
        #path = 'C:/Users/Admin/Desktop/Vertretungsplan/InformatikVertretungsplan/Testdateien/CSVExports/test1.csv'
        self.model.openCSV(path)
        self.update()
        
        

    def on_actionEinlesen_triggered(self):
        pathUnter = QtWidgets.QFileDialog().getOpenFileName(None,"Unter-Daei einlesen","","SPM Files (*.spm);;All Files (*)")[0]
        pathZuordnung = QtWidgets.QFileDialog().getOpenFileName(None,"Zuordnungs-Datei einlesen","","SPM Files (*.spm);;All Files (*)")[0]
        self.model.DateienEinlesen(pathUnter,pathZuordnung)
        self.update()

    
    def update(self):
        pass