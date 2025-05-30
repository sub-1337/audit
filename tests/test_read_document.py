from core.document_reader import DocumentReader
import os

def test1():
    doc = DocumentReader(os.path.join("tests", "test_files", "test_reader.xlsx"))
    doc.readDoc({'year' : 2025, 'month' : 10, 'day' : 11})
    day_name = 'в т о р н и к'
    assert doc.data.processed[1][2] == ''
    for i in range(2, 13 + 1):
        assert doc.data.processed[i][2] == day_name
        assert doc.data.processed[i][1] == ''
        assert doc.data.processed[i][3] == ''
    assert doc.data.processed[14][2] == ''
    print("ok")

def test2():
    doc = DocumentReader(os.path.join("tests", "test_files", "test_reader2.xlsx"))
    doc.readDoc({'year' : 2025, 'month' : 10, 'day' : 11})
    assert (doc.data.processed[1][2] == '') and (doc.data.processed[1][3] == '')
    assert doc.data.processed[2][2] == doc.data.processed[3][2] == doc.data.processed[4][2] == doc.data.processed[5][2] == doc.data.processed[6][2] == 'b d'
    assert doc.data.processed[2][3] == doc.data.processed[3][3] == doc.data.processed[4][3] == doc.data.processed[5][3] == doc.data.processed[6][3] == 'b2 d2'

    assert doc.data.processed[7][2] == doc.data.processed[8][2] == 'q w'

    assert doc.data.processed[7][3] == doc.data.processed[8][3] == 'w'

    assert not doc.data.processed[9][2]
    assert not doc.data.processed[9][3]
    print("ok")

def test():
    try:    
        test1()
    except:
        print("test_reader.xlsx тест не пройден")
    try:
        test2()
    except:
        print("test_reader2.xlsx тест не пройден")