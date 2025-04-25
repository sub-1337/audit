from datetime import date

def test():
    pass
class InputData():
    def __init__(self):
        self.rowMax = 0
        self.colMax = 0
        self.processed = []

"""class Day():
    def __init__(self):
        self.day = 1
        self.month = 1
        self.year = 2000
    def _recalcWeek(self):
        d = date(self.year, self.month, self.day)
        self.week = 
    def setStart(self, day, month, year):
        pass
    def setDayMonthYear(self, day, month, year):
        self.day   = day
        self.month = month 
        self.year  = year
        self._recalcWeek()
    def getDayMothYear(self):
        return (self.day, self.month, self.yea)
    def applyDeltaMonthDay(self, week, dayOfWeek):
        pass
    """

class Auditory():
    def __init__(self, number):
        self.number = number

class CalenderBlock():
    def __init__(self, time, auditory : Auditory):
        self.time = time
        self.auditory = auditory

class CalenderRow():
    def __init__(self):
        self.row = []
    def addBlock(self, block : CalenderBlock):
        self.row.append(block)

class CalenderDay():
    def __init__(self, date : date):
        self.rows = []
        self.date = date
    def addRow(self, row : CalenderRow):
        self.rows.append(row)

class CalenderYear():
    def __init__(self):
        self.allDays= []
    def addDay(self, calenderDay : CalenderDay):        
        self.allDays.append(calenderDay)
    def getDay(self, year, month, day):
        for d in self.allDays:
            if (d.date.year == year) and (d.date.month == month) and (d.date.day == day):
                return d
        return None