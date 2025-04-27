import core.data_model as dm
import datetime as dt

def test():
    calenderDay = dm.CalenderDay(dm.date(2025, 4, 25))

    calenderDay.addBlock(dm.CalenderBlock(dm.Id(1), dt.time(10, 0), dm.Para(1), dm.Auditory("5442")))
    calenderDay.addBlock(dm.CalenderBlock(dm.Id(2), dt.time(10, 0), dm.Para(1), dm.Auditory("5442")))
    calenderDay.addBlock(dm.CalenderBlock(dm.Id(3), dt.time(12, 0), dm.Para(3), dm.Auditory("1442")))
    calenderDay.addBlock(dm.CalenderBlock(dm.Id(4), dt.time(11, 0), dm.Para(2),dm.Auditory("1442")))
    calenderDay.addBlock(dm.CalenderBlock(dm.Id(5), dt.time(14, 0), dm.Para(5), dm.Auditory("3442")))
    dataYear = dm.CalenderYear()
    dataYear.addDay(calenderDay)

    assert(dataYear.getDay(2025, 4, 25) == calenderDay)

    pass

    