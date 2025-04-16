from datetime import datetime

def test():
    pass
class InputData():
    def __init__(self):
        self.rowMax = 0
        self.colMax = 0
        self.processed = []

class Day():
    def __init__(self):
        self.day = 1
        self.month = 1
        self.year = 2000
        self.week = 0
        self.dayofweek = 1
        self.weekInitialized = False
    def _recalcWeek(self):
        pass
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
    

class Calender():
    def __init__(self):
        pass

class CalenderData():
    def __init__(self):
        pass