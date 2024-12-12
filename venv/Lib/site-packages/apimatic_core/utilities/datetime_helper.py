from datetime import datetime, date
from apimatic_core.types.datetime_format import DateTimeFormat


class DateTimeHelper:

    @staticmethod
    def validate_datetime(datetime_value, datetime_format):
        if DateTimeFormat.RFC3339_DATE_TIME == datetime_format:
            return DateTimeHelper.is_rfc_3339(datetime_value)
        elif DateTimeFormat.UNIX_DATE_TIME == datetime_format:
            return DateTimeHelper.is_unix_timestamp(datetime_value)
        elif DateTimeFormat.HTTP_DATE_TIME == datetime_format:
            return DateTimeHelper.is_rfc_1123(datetime_value)

        return False

    @staticmethod
    def validate_date(date_value):
        try:
            if isinstance(date_value, date):
                datetime.strptime(date_value.isoformat(), "%Y-%m-%d")
                return True
            elif isinstance(date_value, str):
                datetime.strptime(date_value, "%Y-%m-%d")
                return True
            else:
                return False
        except ValueError:
            return False

    @staticmethod
    def is_rfc_1123(datetime_value):
        try:
            datetime.strptime(datetime_value, "%a, %d %b %Y %H:%M:%S %Z")
            return True
        except (ValueError, AttributeError, TypeError):
            return False

    @staticmethod
    def is_rfc_3339(datetime_value):
        try:
            if '.' in datetime_value:
                datetime_value = datetime_value[:datetime_value.rindex('.')]
            datetime.strptime(datetime_value, "%Y-%m-%dT%H:%M:%S")
            return True
        except (ValueError, AttributeError, TypeError):
            return False

    @staticmethod
    def is_unix_timestamp(timestamp):
        try:
            datetime.fromtimestamp(float(timestamp))
            return True
        except (ValueError, AttributeError, TypeError):
            return False
