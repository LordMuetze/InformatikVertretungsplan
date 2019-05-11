from PyQt5 import QtWidgets, uic
from model import Vertretungsplan

class MainWindow:

#--------------------------------------------------
    def __init__(self):

        #create main window
        self.app = QtWidgets.QApplication([])
        self.MainWindow = uic.loadUi("Vertretungsplan.ui")
        self.mW = self.MainWindow #Shorter attribute name for shorter code

        #create model and set attribute
        #view calls model, not vice-versa! --> no self.view in model
        self.model = Vertretungsplan()

        #Connections
        #self.mW.{Ausloeser}.{Aktion}.connect({MethodenAufruf})
        #Bsp.: self.mW.pushButton.clicked.connect(self.test)

        #launch GUI --> last step of __init__
        self.MainWindow.show()
        self.app.exec()
#--------------------------------------------------


#--------------------------------------------------
    def test(self):
        print("MainWindow.test() called",end="")
        print(self)
#--------------------------------------------------