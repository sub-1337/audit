from datetime import date
import datetime as dt
from enum import Enum

def test():
    pass
class InputData():
    """
    Данные читаемые из экселя
    """
    def __init__(self):
        self.rowMax = 0
        self.colMax = 0
        self.processed = []

class Auditory():
    """
    Класс аудитории с номером
    """
    def __init__(self, number):
        if number == None:
            self.number = 0
        else:
            self.number = number
    def __hash__(self):
        return hash((self.number))    
    def __eq__(self, other):
        return isinstance(other, Auditory) and self.number == other.number
    def __str__(self):
        return f"{self.number}"
    def __repr__(self):
        return str(self)
    def __lt__(self, other):
        return self.number < other.number
    
class Para():
    """
    Класс номера пары
    """
    def __init__(self, number):
        self.number = number
    def __hash__(self):
        return hash((self.number))    
    def __eq__(self, other):
        return isinstance(other, Para) and self.number == other.number
    def __str__(self):
        return f"Пара номер {self.number}"
    def __repr__(self):
        return str(self)

class Subject():
    """
    Класс предмета (не используется)
    """
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name}"
    def __repr__(self):
        return str(self)

class Professor():
    """
    Класс имени профессора (не используется)
    """
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name}"
    def __repr__(self):
        return str(self)

class Group():
    """
    Класс группы (учеников)
    """
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name}"
    def __repr__(self):
        return str(self)

class Id():
    """
    Класс id объекта данных
    """
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
    """
    Перечисление подгруппы
    """
    DEFAULT = 0
    Group_1 = 1
    Group_2 = 2
    Group_3 = 3
    Group_4 = 4
    def __str__(self):
        if self.value == 0:
            return "По умолчанию"
        if self.value == 1:
            return "1"
        if self.value == 2:
            return "2"
        if self.value == 3:
            return "3"
        if self.value == 4:
            return "4"
    
class RuleEven(Enum):
    """
    Класс чётности/нечётности
    """
    DEFAULT = 0
    # Нечётное
    ODD = 1
    # Нечётное
    EVEN = 2
    # Определённые недели
    # CUSTOM = 3

class DayOfWeek(Enum):
    """
    Класс имени дня недели
    """
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Rule():
    """
    Правило - кирпичик расписания
    """
    def __init__(self, auditory : Auditory, dayOfWeek : DayOfWeek, para : Para, even : RuleEven = RuleEven.DEFAULT, week = [],\
                subgroup : RuleSubgroup = RuleSubgroup.DEFAULT, comment : str = "",confidence : int = 50, group : str = "", originalText : str = "", id : Id = None):
        self.auditory = auditory
        self.even = even
        self.week = week
        self.subgroup = subgroup
        self.dayOfWeek = dayOfWeek   
        self.para = para
        self.comment = comment
        self.confidence = confidence
        self.originalText = originalText
        self.id = id
        self.group = group
    def __str__(self):
        return f"Id {self.id}, auditory {self.auditory}, even {self.even}, week {self.week}, group {self.group}, subgroup {self.subgroup.name}, dayOfWeek {self.dayOfWeek.name}, para {self.para},  comment {self.comment}, confidence {self.confidence}"
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
    """
    Все правила, расписание
    """
    def __init__(self):
        self.rules = []
    def addRule(self, rule : Rule):
        if rule:
            if not rule in self.rules:
                self.rules.append(rule)


class CalenderBlock():
    """
    Блок сущности в календаре по дням
    """
    def __init__(self, id : Id, time, para : Para, auditory : Auditory = None, subGroup : RuleSubgroup = None, comment : str = '', day : date = None, groupBase : Group = None):
        self.id = id
        self.time = time
        self.para = para
        self.auditory = auditory
        self.groupBase = groupBase
        self.subGroup = subGroup        
        self.comment = comment
        self.date = day
        self.overlapWith = []
    def __str__(self):
        return f"calender block: id {self.id}, time {self.time}, para {self.para}, auditory {self.auditory}, group {self.group}, date {self.date}, comment {self.comment}"
    def __repr__(self):
        return str(self)
    def IsSameTime(self, block):
        return self.para == block.para
    def __lt__(self, other):
        return self.date < other.date

class CalenderDay():
    """
    Сущность календаря - один из дней
    """
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
        # Сортировать по аудитории
        arraySorted = sorted(array, key=lambda x: x[0])
        return arraySorted

class AllAuditories():
    """
    Все аудитории (для окна аудиторий)
    """
    def __init__(self):
        self.auditories = {}
    def sort(self):
        self.auditories = dict(sorted(self.auditories.items()))
        for blockKey in self.auditories:
            self.auditories[blockKey] = sorted(self.auditories[blockKey])
    

class CalenderYear():
    """
    Все дни календаря
    """
    def __init__(self):
        self.allDays= []
        self.rules = None
    def addDay(self, calenderDay : CalenderDay):        
        self.allDays.append(calenderDay)
    """def addRules(self, rules : Rules):
        self.rules = rules"""
    def getDay(self, dayDictionary):
        for d in self.allDays:
            if (d.date.year == dayDictionary['year']) and (d.date.month == dayDictionary['month']) and (d.date.day == dayDictionary['day']):
                return d
        return None