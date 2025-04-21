from core.document_reader import DocumentReader
import os

def test():
    doc = DocumentReader(os.path.join("tests", "test_files", "test_reader.xlsx"))
    day_name = 'в т о р н и к'
    assert doc.data.processed[1][2] == ''
    for i in range(2, 13 + 1):
        assert doc.data.processed[i][2] == day_name
        assert doc.data.processed[i][1] == ''
        assert doc.data.processed[i][3] == ''
    assert doc.data.processed[14][2] == ''
    print("ok")