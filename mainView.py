from PyQt5 import QtWidgets, uic
from model import Vertretungsplan

class MainWindow:

    def __init__(self):

        #create main window
        self.app = QtWidgets.QApplication([])
        self.mW = uic.loadUi("mainWindow.ui")

        #create model and set attribute
        #view calls model, not vice-versa! --> no self.view in model
        self.model = Vertretungsplan()

        #Connections
        #self.mainWindow.{Ausloeser}.{Aktion}.connect({MethodenAufruf})
        #Bsp.: self.mainWindow.pushButton.clicked.connect(self.test)
        #self.mainWindow

        #launch GUI --> last step of __init__ because starts loop
        self.mW.show()
        self.app.exec()