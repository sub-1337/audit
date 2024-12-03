#import sys
#import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.calendar import calender

def test():
    cal = calender()

    days = [[2, 2024, 12, 3],
            [3, 2024, 12, 4]]
    for day in days:
        day_in_fact = cal.weekday(year = day[1], month = day[2], day = day[3])
        if day[0] == day_in_fact:
            print("ok", day)
        else:
            print("not ok ", "day is ", day_in_fact," expected ", day)
