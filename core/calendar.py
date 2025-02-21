import calendar

def print_calendar(year, month):
    cal = calendar.TextCalendar(firstweekday=7)
    print(cal.formatmonth(year, month))

def weekday(self, year: int, month: int, day: int) -> int:
    if month < 3:
        year -= 1
        month += 10
    else:
        month -= 2
    res = (day + 31 * month // 12 + year + year // 4 - year // 100 + year // 400) % 7
    if res == 0: # russian calender
        res = 7
    return res