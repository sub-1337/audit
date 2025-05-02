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
    assert(res[0]['auditory']  == dm.Auditory(6254))
    assert(res[1]['auditory']  == dm.Auditory(6254))
    assert(res[0]['even'] == dm.RuleEven.ODD)
    assert(res[1]['even'] == dm.RuleEven.ODD)
    assert(res[0]['subgroup'] == dm.RuleSubgroup(1))
    assert(res[1]['subgroup'] == dm.RuleSubgroup(2))
    assert(res[0]['week'] == [3, 7, 11, 15])
    assert(res[1]['week'] == [5, 9, 13, 17])
    assert(res[0]['confidence'] == 100)
    assert(res[1]['confidence'] == 100)

    cell = "чн.а.6253     Информатика     лаб.                                            доц. Панкратова А.З.  чн. - 3 п/гр."
    res = dr.DocumentReader.parseCell(cell)
    assert(res[0]['auditory']  == dm.Auditory(6253))
    assert(res[0]['even'] == dm.RuleEven.EVEN)
    assert(res[0]['subgroup'] == dm.RuleSubgroup.Group_3)
    assert(res[0]['week'] == [])
    assert(res[0]['confidence'] == 100)
    pass

    

def test():
    #calender()
    rules()
    parseCell()
    pass

    