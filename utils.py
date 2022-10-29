from datetime import datetime
import time


def get_current_datetime():
    """
    Gets stringified datetime in format 'yyyy-mm-dd hh:mm'
    """
    return datetime.today().strftime('%Y-%m-%d %H:%M')


def datetime_to_timestamp(date):
    """
    Given a date in string format 'yyyy-mm-dd hh:mm' it converts it to timestamp
    """
    return time.mktime(datetime.strptime(date, '%Y-%m-%d %H:%M').timetuple())


def timestamp_to_datetime(timestamp):
    """
    Given a timestamp it returns a string date in format 'yyyy-mm-dd hh:mm'
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')



def add_minutes_to_date(date, minutes):
    """
    Adds parameter minutes to a string parameter date
    """
    new_date = datetime_to_timestamp(date) + minutes * 60
    return timestamp_to_datetime(new_date)