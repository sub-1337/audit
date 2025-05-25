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

    cell = """лаб  5422
Конструкторско-технологическое проектирование ЭВМ и комплексов

чн 2 подгр  Макаров Н.Н. 
""" 
    
    res = dr.DocumentReader.parseCell(cell)
    assert res[0]['auditory'] == dm.Auditory(5422)
    assert res[0]['even'] == dm.RuleEven.EVEN
    assert res[0]['subgroup'] == dm.RuleSubgroup.Group_2
    assert res[0]['confidence'] == 100
    
    cell = """нч а.6251, 6254    Инженерная и компьютерная графика     лаб. 1, 2  подгр.      Поспелова Н.В.,  Дроздова Т.А.    	
"""
    res = dr.DocumentReader.parseCell(cell)
    assert res[0]['confidence'] == 100
    assert res[0]['auditory'] == dm.Auditory(6251)
    assert res[0]['subgroup'] == dm.RuleSubgroup(1)
    assert res[1]['auditory'] == dm.Auditory(6254)
    assert res[1]['subgroup'] == dm.RuleSubgroup(2)
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

def rulesToDay2():
    doc = dr.DocumentReader(os.path.join("tests", "test_files", "test_parser2.xlsx"))
    doc.readHead()
    doc.worbookNamesCurrent = doc.worbookNames[0]
    doc.readDoc({'year' : 2025, 'month' : 1, 'day' : 1})
    pass


def groups():
    assert(dr.DocumentReader.isGroup("М24-ИВТ-1 20"))
    assert(dr.DocumentReader.isGroup("М24-ПМ 12"))    
    assert(dr.DocumentReader.isGroup("М24-ИСТ-1  23"))    
    assert(dr.DocumentReader.isGroup("М24-КТЭС 16"))    	
    assert(dr.DocumentReader.isGroup("М24-Р-1 9"))
    assert(dr.DocumentReader.isGroup("М24-ИТС   10"))

    assert(dr.DocumentReader.isGroup("с 24 РЭС    30"))
    assert(dr.DocumentReader.isGroup("24 Р1   18"))
    assert(dr.DocumentReader.isGroup("24 Р2  17"))
    
    assert(dr.DocumentReader.isGroup("24 КТЭС    23	"))    
    assert(dr.DocumentReader.isGroup("24  ИТС   28"))

    assert(dr.DocumentReader.isGroup("24 ИВТ 4 - 1      24"))
    assert(dr.DocumentReader.isGroup("24 ИВТ- 5     24  	"))
    assert(dr.DocumentReader.isGroup("  С24 СИБ    28  	"))
    
    assert(dr.DocumentReader.isGroup("24 ПМ 1      24 	"))
    assert(dr.DocumentReader.isGroup("24 ПМ 2      24 	"))
    assert(dr.DocumentReader.isGroup("24 ИСТ   1 - 1   24 	"))

    assert(dr.DocumentReader.isGroup("23 ИСТ-1-1    18	"))
    assert(dr.DocumentReader.isGroup("С23 РЭС 29	"))
    assert(dr.DocumentReader.isGroup("23 Р2           12	"))
    assert(dr.DocumentReader.isGroup("23 КТЭС 24	"))

    assert(dr.DocumentReader.isGroup("23 ИТС   24	"))
    assert(dr.DocumentReader.isGroup("С 23 СИБ 28	"))
    assert(dr.DocumentReader.isGroup("М23ИСТ-2 9	"))
    assert(dr.DocumentReader.isGroup("М23-КТЭС 14	"))

    assert(dr.DocumentReader.isGroup("22 ССК  (21)	"))
    assert(dr.DocumentReader.isGroup("22 ТР  (10)	"))
    assert(dr.DocumentReader.isGroup("С 22РЭС    (9)	"))
    
    assert(dr.DocumentReader.isGroup("22 ИТД -1  (20)"))    
    assert(dr.DocumentReader.isGroup("22 КТ  (24)	"))    
    assert(dr.DocumentReader.isGroup("22 СБК (37)	"))

    assert(dr.DocumentReader.isGroup("22  СТ (25)	"))
    assert(dr.DocumentReader.isGroup("22 ИС (20)	"))
    assert(dr.DocumentReader.isGroup("22ПО  (20)	"))
    
    assert(dr.DocumentReader.isGroup("22 ВМ  (20)	"))
    assert(dr.DocumentReader.isGroup("21 ИС  30	"))    
    assert(dr.DocumentReader.isGroup("21 ПМ-1  20	"))

def test():
    try:
        rules()
    except:
        print("Тест уникальности не пройден")

    try:
        parseCell()
    except:
        print("Тест на парсинг ячейки не пройден")

    try:
        rulesToDay()
    except:
        print("Тест test_parser.xlsx не пройден")

    try:
        rulesToDay2()    
    except:
        print("Тест test_parser2.xlsx не пройден")
    
    try:
        groups()
    except:
        print("Тест на определение группы не пройден")
    pass

    