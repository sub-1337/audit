import core.data_model as dm
import datetime as dt

def test():
    calenderDay = dm.CalenderDay(dm.date(2025, 4, 25))

    calenderDay.addBlock(dm.CalenderBlock(dt.time(10, 0), dm.Auditory("5442")))
    calenderDay.addBlock(dm.CalenderBlock(dt.time(12, 0), dm.Auditory("1442")))
    calenderDay.addBlock(dm.CalenderBlock(dt.time(14, 0), dm.Auditory("3442")))
    dataYear = dm.CalenderYear()
    dataYear.addDay(calenderDay)

    assert(dataYear.getDay(2025, 4, 25) == calenderDay)

    pass

    