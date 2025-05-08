import core.data_model as dm
import datetime as dt
import core.document_reader as dr
import os

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

def rulesToDay():
    doc = dr.DocumentReader(os.path.join("tests", "test_files", "test_parser.xlsx"))
    doc.readHead()
    doc.worbookNamesCurrent = doc.worbookNames[0]
    doc.readDoc({'year' : 2025, 'month' : 1, 'day' : 1})

    assert(len(doc.rules.rules) == 3)
    assert(doc.rules.rules[0].auditory == dm.Auditory(6246))
    assert(doc.rules.rules[1].auditory == dm.Auditory(6151))
    assert(doc.rules.rules[2].auditory == dm.Auditory(6332))

    assert(doc.rules.rules[0].dayOfWeek == dm.DayOfWeek.MONDAY)
    assert(doc.rules.rules[1].dayOfWeek == dm.DayOfWeek.MONDAY)
    assert(doc.rules.rules[2].dayOfWeek == dm.DayOfWeek.MONDAY)

    assert(len(doc.dataYear.allDays[5].blocks) == 3)
    assert(len(doc.dataYear.allDays[5 + 7].blocks) == 3)
    pass


def test():
    rules()
    parseCell()
    rulesToDay()
    pass

    