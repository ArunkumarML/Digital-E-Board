from datetime import datetime as dt
import pytz
from django.conf import settings
import datetime


def get_current_date_time():
    x = dt.now()
    tz = pytz.timezone(settings.TIME_ZONE)
    return tz.localize(x)


def transform_date_query(request, start_date_name="start_date", end_date_name="end_date"):
    indian_time = pytz.timezone("Asia/Kolkata")
    return (datetime.datetime.combine(datetime.datetime.strptime(request.GET.get(start_date_name), "%Y-%m-%d"),
                                      datetime.time.min).replace(tzinfo=indian_time),
            datetime.datetime.combine(datetime.datetime.strptime(request.GET.get(end_date_name), "%Y-%m-%d"),
                                      datetime.time.max).replace(tzinfo=indian_time))
