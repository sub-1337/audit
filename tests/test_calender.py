#import sys
#import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.calendar import calender

def test():
    cal = calender()
    i = cal.weekday(year = 2024, month = 12, day = 3)
    print(i)
