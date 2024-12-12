from enum import Enum


class DateTimeFormat(Enum):
    """Enumeration of Date time formats

    Attributes:
        HTTP_DATE_TIME: RFC 1123 Date-Time format
        UNIX_DATE_TIME: Unix Timestamp Format
        RFC3339_DATE_TIME: RFC 3339 Date-Time format

    """

    HTTP_DATE_TIME = "HttpDateTime"

    UNIX_DATE_TIME = "UnixDateTime"

    RFC3339_DATE_TIME = "RFC3339DateTime"
