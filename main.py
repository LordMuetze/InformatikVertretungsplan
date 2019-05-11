from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication([])
mainWindow = uic.loadUi("Vertretungsplan.ui")
mainWindow.show()
app.exec()