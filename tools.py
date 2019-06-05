#--------------------------------------------------
    # class containing tools that are used in different classes
    # methods should always be staticmethods
#--------------------------------------------------
class Tools:
    @staticmethod
    # return 2-dimensional list --> sortet week-list consists of day-lists consists of sortet lessons
    def sortStundenliste(stundenliste:list):
        returnList = [[],[],[],[],[]]
        stundenliste.sort(key=lambda c: c.getStunde()) #sort stundenliste by lessonnumber on that day
        for stunde in stundenliste:
            returnList[stunde.Tag()].append(stunde)
        return returnList
#--------------------------------------------------
#--------------------------------------------------