__author__ = 'Antonio'


from datetime import datetime
from pytz import timezone

fmt = "%Y-%m-%d %H:%M:%S %Z%z"
# fmt = "%Y-%m-%d %H:%M:%S %Z"

# Current time in UTC
# now_utc = datetime.now(timezone('UTC'))
curr_time_wo_tz = datetime.strptime('2011-01-21 02:37:21', '%Y-%m-%d %H:%M:%S')
curr_time_with_tz = timezone('US/Pacific').localize(curr_time_wo_tz)

print("curr_time_wo_tz", curr_time_wo_tz.strftime(fmt))
print("curr_time_with_tz", curr_time_with_tz.strftime(fmt))

# Convert to UTC time zone
now_pacific = curr_time_with_tz.astimezone(timezone('UTC'))
print("now_pacific", now_pacific.strftime(fmt))

# Convert to Europe/Moscow time zone
now_moscow = now_pacific.astimezone(timezone('Europe/Moscow'))
print("now_moscow", now_moscow.strftime(fmt))

