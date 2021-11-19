from collections import namedtuple
from datetime import datetime

import arrow
from dateutil.relativedelta import relativedelta
from pytz import utc


class WindowPeriod:
    def __init__(
        self,
        rlower: relativedelta,
        rupper: relativedelta,
    ):
        self.rlower = rlower
        self.rupper = rupper

    def get_window(self, dt: datetime):
        """Returns a named tuple of the lower and upper values."""
        dt_floor = arrow.get(dt).to("utc").replace(hour=0, minute=0).datetime
        dt_ceil = arrow.get(dt).to("utc").replace(hour=23, minute=59).datetime
        Window = namedtuple("window", ["lower", "upper"])
        return Window(dt_floor - self.rlower, dt_ceil + self.rupper)

    def in_window(
        self,
        report_datetime: datetime,
        timepoint_datetime: datetime,
    ):
        window = self.get_window(dt=timepoint_datetime)
        return window.lower <= report_datetime.astimezone(utc) <= window.upper
