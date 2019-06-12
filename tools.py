#--------------------------------------------------
    # class containing tools that are used in different classes
    # methods should always be staticmethods
#--------------------------------------------------
class Tools:
    @staticmethod
    # return 2-dimensional list --> sortet week-list consists of day-lists consists of sortet lessons
    def sortStundenliste(stundenliste:list):
        returnList = [[],[],[],[],[]]
        stundenliste.sort(key=lambda c: c.Stunde()) #sort stundenliste by lessonnumber on that day
        for stunde in stundenliste:
            returnList[stunde.Tag()].append(stunde)
        return returnList

    @staticmethod
    def convertWeekdayGerman(day):
        #weekday as string
        if day == "Mo":
            dayformatted = 0
        elif day == "Di":
            dayformatted = 1
        elif day == "Mi":
            dayformatted = 2
        elif day == "Do":
            dayformatted = 3
        elif day == "Fr":
            dayformatted = 4
        elif day == "Sa":
            dayformatted = 5
        elif day == "So":
            dayformatted = 6

        elif day == 0:
            dayformatted = "Mo"
        elif day == 1:
            dayformatted = "Di"
        elif day == 2:
            dayformatted = "Mi"
        elif day == 3:
            dayformatted = "Do"
        elif day == 4:
            dayformatted = "Fr"
        elif day == 5:
            dayformatted = "Sa"
        elif day == 6:
            dayformatted = "So"

        else:
            dayformatted = None

        return dayformatted
#--------------------------------------------------
#--------------------------------------------------