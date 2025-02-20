from core.document_reader import DocumentReader
from core.gui import GUI_input_show
import os

def test():    
    reader = DocumentReader(os.path.join("tests", "test_files", "test_whole.xlsx"))
    GUI_input_show(reader.data)
