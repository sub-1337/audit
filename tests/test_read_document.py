from core.document_reader import DocumentReader
import os
def test():
    doc = DocumentReader(os.path.join("data", "test_reader.xlsx"))
    day_name = 'в т о р н и к'
    assert doc.processed[1][2] == None
    for i in range(2, 13 + 1):
        assert doc.processed[i][2] == day_name
        assert doc.processed[i][1] == None
        assert doc.processed[i][3] == None
    assert doc.processed[14][2] == None
    pass