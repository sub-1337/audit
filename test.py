from tests.test_calender import test as test_cal
print("---Test of week day---")
test_cal()

from tests.test_read_document import test as test_reader
print("---Test of reader---")
test_reader()

"""import sys
if len(sys.argv) >= 2:
    if (sys.argv[1] == "--gui"):
        from tests.test_gui import test as test_gui
        print("---Test of gui---")
        test_gui()"""

from tests.test_gui import test as test_gui
print("---Test of gui---")
test_gui()