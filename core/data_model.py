from datetime import date
import datetime as dt

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
    def __hash__(self):
        return hash((self.number))    
    def __eq__(self, other):
        return isinstance(other, Auditory) and self.number == other.number
    def __str__(self):
        return f"{self.number}"
    def __repr__(self):
        return str(self)
    
class Para():
    def __init__(self, number):
        self.number = number
        self.markedOverlap = False
    def __hash__(self):
        return hash((self.number))    
    def __eq__(self, other):
        return isinstance(other, Para) and self.number == other.number
    def __str__(self):
        return f"para {self.number}"
    def __repr__(self):
        return str(self)

class Subject():
    def __init__(self):
        pass

class Professor():
    def __init__(self):
        pass

class Group():
    def __init__(self):
        pass

class CalenderBlock():
    def __init__(self, time, para : Para, auditory : Auditory, subject : Subject, professor : Professor, group : Group):
        self.time = time
        self.para = para
        self.auditory = auditory
        self.subject = subject
        self.professor = professor
        self.group = group
    def __str__(self):
        return f"calender: time {self.time}, para {self.para}, auditory {self.auditory}, subject {self.subject}, professor {self.professor}, group {self.group}"
    def __repr__(self):
        return str(self)

class CalenderDay():
    def __init__(self, date : date):
        self.blocks = []
        self.date = date
    def addBlock(self, block : CalenderBlock):
        self.blocks.append(block)
    def sizeBlocks(self):
        return len(self.blocks)
    def getDate(self):
        return self.date
    def CalcArrayByAudirory(self):
        self.auditories = {}
        self.auditoriesWarning = {}
        
        for block in self.blocks:
            auditory: Auditory = block.auditory
            time: dt.datetime.time = block.time
            para: Para = block.para
            if (self.auditories.get(auditory) is None):
                self.auditories[auditory] = [(time, para,)]
            else:
                self.auditories[auditory].append((time, para,))
        for auditorie, time in self.auditories.items():
            for i in range(len(time)):
                for j in range(len(time)):
                    if i != j and time[i] == time[j]:
                        if (self.auditoriesWarning.get(auditory) is None):
                            self.auditoriesWarning[auditorie] = [time[i]]
                        else:
                            self.auditoriesWarning[auditorie].append(time[i])
        for auditorie, time in self.auditories.items():
            time.sort()
        pass
        
    def ReturnArrayByAuditory(self):
        self.CalcArrayByAudirory()

        rows, cols = len(self.auditories), 7
        array = [["" for _ in range(cols)] for _ in range(rows)]

        for i in range(len(array)):
            auditory, time = list(self.auditories.items())[i]
            array[i][0] = auditory
            j = 1
            for v in time:
                n = v[1].number
                array[i][n] = v[1]
                #if self.auditoriesWarning[auditory]
                if self.auditoriesWarning.get(auditory):
                    array[i][n].markedOverlap = True
                j += 1
        return array
           



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