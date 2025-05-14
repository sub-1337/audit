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
    assert doc.data.processed[2][2] == doc.data.processed[3][2] == doc.data.processed[4][2] == doc.data.processed[5][2] == doc.data.processed[6][2] == "abd"
    assert doc.data.processed[2][3] == doc.data.processed[3][3] == doc.data.processed[4][3] == doc.data.processed[5][3] == doc.data.processed[6][3] == "a2b2d2"
    assert not doc.data.processed[8][2]
    assert not doc.data.processed[8][3]
    assert not doc.data.processed[1][2]
    assert not doc.data.processed[1][3]
    print("ok")

def test():
    test1()
    test2()