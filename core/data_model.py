from datetime import date
import datetime as dt
from enum import Enum

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
    def __hash__(self):
        return hash((self.number))    
    def __eq__(self, other):
        return isinstance(other, Para) and self.number == other.number
    def __str__(self):
        return f"para {self.number}"
    def __repr__(self):
        return str(self)

class Subject():
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name}"
    def __repr__(self):
        return str(self)

class Professor():
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name}"
    def __repr__(self):
        return str(self)

class Group():
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name}"
    def __repr__(self):
        return str(self)

class Id():
    def __init__(self, idNumber):
        self.idNumber = idNumber
    def __hash__(self):
        return hash((self.idNumber))    
    def __eq__(self, other):
        return isinstance(other, Id) and self.idNumber == other.idNumber
    def __str__(self):
        return f"{self.idNumber}"
    def __repr__(self):
        return str(self)

class RuleSubgroup(Enum):
    DEFAULT = 0
    Group_1 = 1
    Group_2 = 2
    Group_3 = 3
    Group_4 = 4
    
class RuleEven(Enum):
    DEFAULT = 0
    # Нечётное
    ODD = 1
    # Нечётное
    EVEN = 2
    # Определённые недели
    CUSTOM = 3

class DayOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Rule():
    def __init__(self, auditory : Auditory, dayOfWeek : DayOfWeek, para : Para, even : RuleEven = RuleEven.DEFAULT, week = [],  subgroup : RuleSubgroup = RuleSubgroup.DEFAULT, id : Id = None):
        self.auditory = auditory
        self.even = even
        self.week = week
        self.subgroup = subgroup
        self.dayOfWeek = dayOfWeek   
        self.para = para
        self.id = id
    def __str__(self):
        return f"Id {self.id}, auditory {self.auditory}, even {self.even}, week {self.week}, subgroup {self.subgroup.name}, dayOfWeek {self.dayOfWeek.name}, para {self.para}"
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        if isinstance(other, Rule):
            return \
            self.auditory == other.auditory and \
            self.even == other.even and \
            self.week == other.week and \
            self.subgroup == other.subgroup and \
            self.dayOfWeek == other.dayOfWeek and \
            self.para == other.para and \
            self.id == other.id

class Rules():
    def __init__(self):
        self.rules = []
    def addRule(self, rule : Rule):
        if rule:
            if not rule in self.rules:
                self.rules.append(rule)


class CalenderBlock():
    def __init__(self, id : Id, time, para : Para, auditory : Auditory, subject : Subject, professor : Professor, group : Group):
        self.id = id
        self.time = time
        self.para = para
        self.auditory = auditory
        self.subject = subject
        self.professor = professor
        self.group = group
        self.overlapWith = []
    def __str__(self):
        return f"calender block: id {self.id}, time {self.time}, para {self.para}, auditory {self.auditory}, subject {self.subject}, professor {self.professor}, group {self.group}"
    def __repr__(self):
        return str(self)
    def IsSameTime(self, block):
        return self.para == block.para

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
        
        for block in self.blocks:
            auditory: Auditory = block.auditory
            time: dt.datetime.time = block.time
            para: Para = block.para
            if (self.auditories.get(auditory) is None):
                self.auditories[auditory] = [block]
            else:
                self.auditories[auditory].append(block)
        for auditorie, blocks in self.auditories.items():
            for i in range(len(blocks)):
                for j in range(len(blocks)):
                    if i != j and blocks[i].IsSameTime(blocks[j]):
                        blocks[i].overlapWith.append(blocks[j].id)
        """for auditorie, blocks in self.auditories.items():
            blocks.sort()
        pass"""
        
    def ReturnArrayByAuditory(self):
        self.CalcArrayByAudirory()

        rows, cols = len(self.auditories), 7
        array = [["" for _ in range(cols)] for _ in range(rows)]

        for i in range(len(array)):
            auditory, blocks = list(self.auditories.items())[i]
            array[i][0] = auditory
            j = 1
            for block in blocks:
                n = block.para.number
                array[i][n] = block
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