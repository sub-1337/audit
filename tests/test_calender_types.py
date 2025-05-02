import core.data_model as dm
import datetime as dt
import core.document_reader as dr

# Поломано
def calender():
    calenderDay = dm.CalenderDay(dm.date(2025, 4, 25))

    calenderDay.addBlock(dm.CalenderBlock(dm.Id(1), dt.time(10, 0), dm.Para(1), dm.Auditory("5442")))
    calenderDay.addBlock(dm.CalenderBlock(dm.Id(2), dt.time(10, 0), dm.Para(1), dm.Auditory("5442")))
    calenderDay.addBlock(dm.CalenderBlock(dm.Id(3), dt.time(12, 0), dm.Para(3), dm.Auditory("1442")))
    calenderDay.addBlock(dm.CalenderBlock(dm.Id(4), dt.time(11, 0), dm.Para(2),dm.Auditory("1442")))
    calenderDay.addBlock(dm.CalenderBlock(dm.Id(5), dt.time(14, 0), dm.Para(5), dm.Auditory("3442")))
    dataYear = dm.CalenderYear()
    dataYear.addDay(calenderDay)

    assert(dataYear.getDay(2025, 4, 25) == calenderDay)

def rules():
    rules = dm.Rules()

    rules.addRule(rules.addRule(dm.Rule(dm.Auditory("5442"), dm.DayOfWeek.MONDAY, dm.Para(1), dm.RuleEven.DEFAULT, None, dm.RuleSubgroup.DEFAULT)))
    rules.addRule(rules.addRule(dm.Rule(dm.Auditory("5442"), dm.DayOfWeek.MONDAY, dm.Para(1), dm.RuleEven.DEFAULT, None, dm.RuleSubgroup.DEFAULT)))
    
    assert(len(rules.rules) == 1)

    pass

def parseCell():
    cell = "нч. а.6254     Информатика     лаб.   .     Панкратова А.З.                        1 подгр  3,7,11,15  нед                                       2 подгр  5,9,13,17  нед "
    res = dr.DocumentReader.parseCell(cell)
    pass

def test():
    #calender()
    rules()
    parseCell()
    pass

    