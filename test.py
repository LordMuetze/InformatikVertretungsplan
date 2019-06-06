import classes

s = classes.Stunde(0,0,"5a","L1","AE05","M")
print(s)



Exception has occurred: AttributeError
'Stunde' object has no attribute 'fach'
  File "C:\Users\Admin\Desktop\Vertretungsplan\InformatikVertretungsplan\classes.py", line 74, in Fach
    return self.fach
  File "C:\Users\Admin\Desktop\Vertretungsplan\InformatikVertretungsplan\classes.py", line 223, in addStunde
    if stunde.Fach() not in self.faecherliste:
  File "C:\Users\Admin\Desktop\Vertretungsplan\InformatikVertretungsplan\classes.py", line 210, in __init__
    self.addStunde(stunde)
  File "C:\Users\Admin\Desktop\Vertretungsplan\InformatikVertretungsplan\classes.py", line 193, in createLehrer
    return Lehrer(bezeichner,stunde)
  File "C:\Users\Admin\Desktop\Vertretungsplan\InformatikVertretungsplan\classes.py", line 33, in __init__
    self.lehrer = Lehrer.createLehrer(lehrer,self)
  File "C:\Users\Admin\Desktop\Vertretungsplan\InformatikVertretungsplan\test.py", line 3, in <module>
    s = classes.Stunde(0,0,"5a","L1","AE05","M")