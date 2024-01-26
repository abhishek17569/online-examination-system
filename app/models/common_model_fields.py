from flask_restx import fields

from app.utils.custom_fields import TZDateTimeField

id = fields.String(title="Id", example="65a5728b663d5c7050b6295a")

tz_datetime = TZDateTimeField(
    title="Datetime in ISO8601 TZ format", example="2023-03-02T06:09:05.092000Z"
)
