

class calender():
    def weekday(self, year: int, month: int, day: int) -> int:
        if month < 3:
            year -= 1
            month += 10
        else:
            month -= 2
        return (day + 31 * month // 12 + year + year // 4 - year // 100 + year // 400) % 7
    def __init__(self):
        pass