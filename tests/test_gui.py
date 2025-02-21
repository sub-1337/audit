from core.control import CreateDocument
from core.gui import GUI_input_show, GUI_main_window_show, GUI_calender_window_show
from core.data_model import CalenderData
import os

def test():  
#    GUI_main_window_show()  
#    doc = CreateDocument(os.path.join("tests", "test_files", "test_whole.xlsx"))
#    GUI_input_show(doc)
    calenderData = CalenderData()
    GUI_calender_window_show(calenderData)
