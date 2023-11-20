# ****************************************************************************
#
# Copyright (C) 2019-2023, ShakeLab Developers.
# This file is part of ShakeLab.
#
# ShakeLab is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# ShakeLab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# with this download. If not, see <http://www.gnu.org/licenses/>
#
# ****************************************************************************
"""
Time and date functionalities
"""

# CONSTANTS
MSEC = 60.
HSEC = 3600.
DSEC = 86400.
YDAYS = 365.

from decimal import Decimal
from shakelab.libutils.timezones import TIMEZONE

class Date(object):
    """
    Note: error is in seconds
    """

    def __init__(self, date=None, format='calendar', error=0., timezone='UTC'):
        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.second = None
        self.error = error

        if date is not None:
            self.set_date(date, format=format)

    def __eq__(self, value):
        """
        """
        t0 = self.to_seconds(decimal=True)
        if isinstance(value, Date):
            t1 = value.to_seconds(decimal=True)
        else:
            t1 = Decimal(value)

        return (t0 == t1)

    def __lt__(self, value):
        """
        """
        t0 = self.to_seconds(decimal=True)
        if isinstance(value, Date):
            t1 = value.to_seconds(decimal=True)
        else:
            t1 = Decimal(value)

        return (t0 < t1)


    def __le__(self, value):
        """
        """
        t0 = self.to_seconds(decimal=True)
        if isinstance(value, Date):
            t1 = value.to_seconds(decimal=True)
        else:
            t1 = Decimal(value)

        return (t0 <= t1)

    def __gt__(self, value):
        """
        """
        t0 = self.to_seconds(decimal=True)
        if isinstance(value, Date):
            t1 = value.to_seconds(decimal=True)
        else:
            t1 = Decimal(value)

        return (t0 > t1)

    def __ge__(self, value):
        """
        """
        t0 = self.to_seconds(decimal=True)
        if isinstance(value, Date):
            t1 = value.to_seconds(decimal=True)
        else:
            t1 = Decimal(value)

        return (t0 >= t1)


    def __add__(self, value):
        """
        """
        if isinstance(value, (int, float)):
            t0 = self.to_seconds(decimal=True)
            t1 = Decimal(value)
            return Date(float(t0 + t1))

        elif isinstance(value, Date):
            t0 = self.to_seconds(decimal=True)
            t1 = value.to_seconds(decimal=True)
            return float(t0 + t1)

        else:
            print('Not a supported operation.')
            return None

    def __sub__(self, value):
        """
        """
        if isinstance(value, (int, float)):
            t0 = self.to_seconds(decimal=True)
            t1 = Decimal(value)
            return Date(float(t0 - t1))

        elif isinstance(value, Date):
            t0 = self.to_seconds(decimal=True)
            t1 = value.to_seconds(decimal=True)
            return float(t0 - t1)

        else:
            print('Not a supported operation.')
            return None

    def __repr__(self):
        """
        """
        return self.get_date(dtype='string')

    def set_date(self, date, format='calendar'):
        """
        added parsing date as ISO8601 string (calendar and ordinal)
        TO DO: create an external syntax parser
        """
        if isinstance(date, (list, tuple)):

            if date[0] >= 1:
                self.year = int(date[0])
            else:
                raise ValueError('Year must be > 1')

            if date[1] >= 1 and date[1] <= 12:
                self.month = int(date[1])
            else:
                raise ValueError('Month must be between 1 and 12')

            if date[2] >= 1 and date[2] <= 31:
                self.day = int(date[2])
            else:
                raise ValueError('Day must be between 1 and 31')

            if date[3] >= 0 and date[3] <= 23:
                self.hour = int(date[3])
            else:
                raise ValueError('Hours must be between 0 and 23')

            if date[4] >= 0 and date[4] <= 59:
                self.minute = int(date[4])
            else:
                raise ValueError('Minutes must be between 0 and 59')

            if date[5] >= 0 and date[5] < 60:
                self.second = float(date[5])
            else:
                raise ValueError('Seconds must be between 0 and 60')

            if len(date) > 6:
                tzinfo = str(date[6])
                if tzinfo in TIMEZONE.keys():
                    self.shift_time(-TIMEZONE[tzinfo]['delay'], units='h')


        elif isinstance(date, dict):

            self.year = date['year']
            self.day = date['day']
            self.hour = date['hour']
            self.minute = date['minute']
            self.second = date['second']

            if format in ('ordinal', 'julian'):
                (self.month, self.day) = days_to_month(self.year, self.day)
            else:
                self.month = date['month']

            try:
                tzinfo = date['tzinfo']
                if tzinfo in TIMEZONE.keys():
                    self.shift_time(-TIMEZONE[tzinfo]['delay'], units='h')
            except:
                pass

        elif isinstance(date, str):

            date = date.replace('-', '')
            date = date.replace(':', '')
            date = date.replace('T', '', 1)

            tzinfo = ''.join(filter(lambda z: z not in '0123456789.', date))
            date = ''.join(filter(lambda z: z in '0123456789.', date))

            if format in ('calendar', 'gregorian'):
                self.year = int(date[0:4])
                self.month = int(date[4:6])
                self.day = int(date[6:8])
                self.hour = int(date[8:10])
                self.minute = int(date[10:12])
                self.second = float(date[12:])

            if format in ('ordinal', 'julian'):
                self.year = int(date[0:4])
                julian_day = int(date[4:7])
                self.hour = int(date[7:9])
                self.minute = int(date[9:11])
                self.second = float(date[11:])

                # Convert total days to month/day
                (self.month, self.day) = days_to_month(self.year, julian_day)

            # Apply UTC conversion
            if tzinfo in TIMEZONE.keys():
                self.shift_time(-TIMEZONE[tzinfo]['delay'], units='h')

        elif isinstance(date, (int, float, Decimal)):

            self.from_seconds(date)

        else:
            raise ValueError('Format not recognized')

    def get_date(self, dtype='list', format='calendar'):
        """
        Returns date in UTC time
        """
        if dtype in ('l', 'list'):

            date = [self.year, self.month, self.day,
                    self.hour, self.minute, self.second]

        elif dtype in ('s', 'str', 'string'):

            # ISO-8601 format
            date = '{0:04d}-'.format(self.year)
            date += '{0:02d}-'.format(self.month)
            date += '{0:02d}T'.format(self.day)
            date += '{0:02d}:'.format(self.hour)
            date += '{0:02d}:'.format(self.minute)
            date += '{0:07.4f}'.format(self.second)

        else:
            raise ValueError('Format not recognized')

        return date

    def to_seconds(self, decimal=False):
        """
        """
        return date_to_sec(self.year, self.month, self.day,
                           self.hour, self.minute, self.second,
                           decimal=decimal)
    @property
    def seconds(self):
        """
        """
        return self.to_seconds()

    def from_seconds(self, second):
        """
        """
        self.set_date(sec_to_date(float(second)))

    def shift_time(self, time, units='s'):
        """
        """
        if units in ['s', 'second', 'seconds']:
            seconds = time
        elif units in ['m', 'minute', 'minutes']:
            seconds = time * MSEC
        elif units in ['h', 'hour', 'hours']:
            seconds = time * HSEC
        elif units in ['d', 'day', 'days']:
            seconds = time * DSEC
        else:
            print('Time units not yet implemented')

        self.from_seconds(self.to_seconds() + seconds)

def leap_check(year):
    """
    Check if leap year.
    """
    c0 = (year % 4 == 0)
    c1 = (year % 100 != 0)
    c2 = (year % 400 == 0)

    return (c0 and c1) or c2

def leap_num(year):
    """
    Compute the number of leap years before current year
    (starting from 1 a.c.)
    """
    n0 = (year-1)//4
    n1 = (year-1)//100
    n2 = (year-1)//400

    return n0 - n1 + n2

def days_in_month(year):
    """
    """
    if leap_check(year):
        mdays = [31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    else:
        mdays = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]

    return mdays

def date_to_sec(year=1, month=1, day=1, hour=0, minute=0, second=0.0,
                decimal=False):
    """
    Convert a date to seconds.
    Not yet implemented for b.c. years.
    """

    if year < 1:
      print('Error: Year must be positive (> 1)')
      return None

    #MDAYS = [0] + days_in_month(2012)[:-1]
    MDAYS = [0] + days_in_month(year)[:-1]    # TO CHECK

    ysec = (year - 1) * YDAYS * DSEC
    ysec += leap_num(year) * DSEC
    msec = MDAYS[int(month) - 1] * DSEC
    dsec = (day - 1) * DSEC

    sec = ysec + msec + dsec + hour*HSEC+ minute*MSEC

    if decimal:
        return Decimal(sec) + Decimal(second)
    else:
        return sec + second

def days_to_month(year, day):
    """
    """
    MDAYS = days_in_month(year)

    for m, d in enumerate(MDAYS):
        if day <= d:
            month = m + 1
            if m > 0:
                day -= MDAYS[m - 1]
            break

    return (month, day)

def sec_to_date(second):
    """
    Implemented using a direct search approach
    (it would be nicer to use a more elengant algorithm).
    """
    # Loop over years (accounting for leap days)
    year = 0
    while True:
        year += 1
        secy = YDAYS * DSEC
        if leap_check(year):
            secy += DSEC
        if second >= secy:
            second -= secy
        else:
            break

    # Number of total days in the last year
    day = (second // DSEC) + 1

    # Find month corresponding to day of the year
    MDAYS = days_in_month(year)

    for m, d in enumerate(MDAYS):
        if day <= d:
            month = m + 1
            if m > 0:
                day -= MDAYS[m - 1]
                second -= MDAYS[m - 1] * DSEC
            break
    second -= (day - 1) * DSEC

    # Hours
    hour = second // HSEC
    second -= hour * HSEC

    # Minutes
    minute = second // MSEC
    second -= minute * MSEC

    return [int(year), int(month), int(day),
            int(hour), int(minute), second]

