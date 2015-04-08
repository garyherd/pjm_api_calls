# TODO: implement daylight savings logic
# Mar: UTC5 - UCT3
# Mar - Nov: UTC4 = UTC3
# Nov: UTC4 - UTC4A
# Nov - Mar: UTC5 - UTC4

from dateutil import parser, tz
from datetime import datetime, time


def process_UTC(utc_string):
    utc_date = parser.parse(utc_string)
    local_time_zone = tz.gettz('US/Eastern')
    local_dt = utc_date.astimezone(local_time_zone)
    local_ds = local_dt.strftime('%m/%d/%Y')
    local_hour = local_dt.time().hour + 1
    return utc_date, local_dt, local_ds, local_hour


def UTC_to_date_string(utc_string):
    utc_date = parser.parse(utc_string)
    local_time_zone = tz.gettz('US/Eastern')
    local_dt = utc_date.astimezone(local_time_zone)
    local_ds = local_dt.strftime('%m/%d/%Y')
    return local_ds


def UTC_to_local_hour(utc_string):
    utc_date = parser.parse(utc_string)
    local_time_zone = tz.gettz('US/Eastern')
    local_dt = utc_date.astimezone(local_time_zone)
    return local_dt.time().hour + 1


# utc_strings = [
#     "2014-11-02T04:00:00Z",
#     "2014-11-02T05:00:00Z",
#     "2014-11-02T06:00:00Z",
#     "2014-11-02T07:00:00Z",
#     "2014-11-02T08:00:00Z",
#     "2014-03-08T05:00:00Z",
#     "2014-03-08T06:00:00Z",
#     "2014-03-08T07:00:00Z",
#     "2014-03-08T08:00:00Z",
#     "2014-03-08T09:00:00Z",
#     "2014-03-08T10:00:00Z",
#     "2014-03-08T11:00:00Z",
#     "2014-03-08T12:00:00Z",
#     "2014-03-08T13:00:00Z",
#     "2014-03-08T14:00:00Z",
#     "2014-03-08T15:00:00Z",
#     "2014-03-08T16:00:00Z",
#     "2014-03-08T17:00:00Z",
#     "2014-03-08T18:00:00Z",
#     "2014-03-08T19:00:00Z",
#     "2014-03-08T20:00:00Z",
#     "2014-03-08T21:00:00Z",
#     "2014-03-08T22:00:00Z",
#     "2014-03-08T23:00:00Z",
#     "2014-03-09T00:00:00Z",
#     "2014-03-09T01:00:00Z",
#     "2014-03-09T02:00:00Z",
#     "2014-03-09T03:00:00Z",
#     "2014-03-09T04:00:00Z",
#     "2014-03-09T05:00:00Z",
#     "2014-03-09T06:00:00Z",
#     "2014-03-09T07:00:00Z",
#     "2014-03-09T08:00:00Z",
#     "2014-03-09T09:00:00Z",
#     "2014-03-09T10:00:00Z",
#     "2014-03-09T11:00:00Z",
#     "2014-03-09T12:00:00Z",
#     "2014-03-09T13:00:00Z",
#     "2014-03-09T14:00:00Z",
#     "2014-03-09T15:00:00Z",
#     "2014-03-09T16:00:00Z",
#     "2014-03-09T17:00:00Z",
#     "2014-03-09T18:00:00Z",
#     "2014-03-09T19:00:00Z",
#     "2014-03-09T20:00:00Z",
#     "2014-03-09T21:00:00Z",
#     "2014-03-09T22:00:00Z",
#     "2014-03-09T23:00:00Z",
#     "2014-03-10T00:00:00Z",
#     "2014-03-10T01:00:00Z",
#     "2014-03-10T02:00:00Z",
#     "2014-03-10T03:00:00Z",
#     "2014-03-10T04:00:00Z",
#     "2014-03-10T05:00:00Z",
#     "2014-03-10T06:00:00Z",
#     "2014-03-10T07:00:00Z",
#     "2014-03-10T08:00:00Z",
#     "2014-03-10T09:00:00Z",
#     "2014-03-10T10:00:00Z",
#     "2014-03-10T11:00:00Z",
#     "2014-03-10T12:00:00Z",
#     "2014-03-10T13:00:00Z",
#     "2014-03-10T14:00:00Z",
#     "2014-03-10T15:00:00Z",
#     "2014-03-10T16:00:00Z",
#     "2014-03-10T17:00:00Z",
#     "2014-03-10T18:00:00Z",
#     "2014-03-10T19:00:00Z",
#     "2014-03-10T20:00:00Z",
#     "2014-03-10T21:00:00Z",
#     "2014-03-10T22:00:00Z",
#     "2014-03-10T23:00:00Z",
#     "2014-03-11T00:00:00Z",
#     "2014-03-11T01:00:00Z",
#     "2014-03-11T02:00:00Z",
#     "2014-03-11T03:00:00Z"]
#
# for u_date in utc_strings:
#     utc_date, local_datetime, local_date, local_hr = process_UTC(u_date)
#     print("{0}    {1}    {2}     {3}".format(utc_date, local_datetime, local_date, local_hr))


