#import sys
#import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.calendar import weekday, print_calendar

def test():

    print_calendar(2025, 2)

    # day of week / year / month / day of month
    days = [[2, 2024, 12, 3],
            [3, 2024, 12, 4],
            [7, 2024, 12, 29],
            [3, 2025, 1, 1],
            [6, 2027, 5, 1]]
    for day in days:
        day_in_fact = weekday(year = day[1], month = day[2], day = day[3])
        if day[0] == day_in_fact:
            print("ok", day)
        else:
            print("not ok ", "day is ", day_in_fact," expected ", day)
