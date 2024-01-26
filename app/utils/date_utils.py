from datetime import datetime


def get_datetime_object_from_string(date_str: str) -> datetime:
    """
    Returns a datetime object of the date time string passed in the format
    %Y-%m-%dT%H:%M:%S.%fZ. Other formats would result in a ValueError.

    :param date_str: str, date-time string

    :return: datetime, parsed datetime object

    :raises ValueError: if the timestamp format is supplied is incorrect
    """

    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
