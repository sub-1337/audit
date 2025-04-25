import core.data_model as dm
import datetime as dt

def test():
    calenderDay = dm.CalenderDay(dt.date(2025, 4, 17))
    row1 = dm.CalenderRow()
    row2 = dm.CalenderRow()

    row1.addBlock(dm.CalenderBlock(dt.time(10, 0), dm.Auditory("5442")))
    row1.addBlock(dm.CalenderBlock(dt.time(12, 0), dm.Auditory("1442")))
    row1.addBlock(dm.CalenderBlock(dt.time(14, 0), dm.Auditory("3442")))
    calenderDay.addRow(row1)

    row2.addBlock(dm.CalenderBlock(dt.time(10, 0), dm.Auditory("6112")))
    calenderDay.addRow(row2)

    calenderYear = dm.CalenderYear()
    calenderYear.addDay(calenderDay)

    assert(calenderYear.getDay(2025, 4, 17) == calenderDay)

    pass

    