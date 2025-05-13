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
    assert len(doc.data.processed[2][2]) > 25
    assert len(doc.data.processed[2][3]) > 25
    print("ok")

def test():
    #test1()
    test2()