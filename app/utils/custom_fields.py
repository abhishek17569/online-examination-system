from datetime import datetime

from flask_restx.fields import DateTime, MarshallingError


class TZDateTimeField(DateTime):
    """
    Custom datetime marshal field to return the datetime in iso8601 format
    appended with "Z" e.g. 2023-03-02T06:09:05.092000Z.

    :raises MarshallingError: If dt_format is set to anything other than iso8601
    """

    def __init__(self, **kwargs):
        if kwargs.get("dt_format", "iso8601") != "iso8601":
            raise MarshallingError("TZDateTimeField only supports iso8601 format")
        super().__init__(**kwargs)

    def format_iso8601(self, dt: datetime) -> str:
        """
        Turn a datetime object into an ISO8601 TZ formatted date.

        :param datetime dt: The datetime to transform
        :return: A ISO 8601 TZ formatted date string
        """
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
