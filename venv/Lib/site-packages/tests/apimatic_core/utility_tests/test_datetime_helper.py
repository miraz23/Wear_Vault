from datetime import datetime, date
import pytest
from apimatic_core.types.datetime_format import DateTimeFormat
from apimatic_core.utilities.api_helper import ApiHelper
from apimatic_core.utilities.datetime_helper import DateTimeHelper


class TestDateTimeHelper:

    @pytest.mark.parametrize('input_dt, input_datetime_format, expected_output', [
        ('1994-11-06T08:49:37', DateTimeFormat.RFC3339_DATE_TIME, True),
        ('1994-02-13T14:01:54.656647Z', DateTimeFormat.RFC3339_DATE_TIME, True),
        ('Sun, 06 Nov 1994 03:49:37 GMT', DateTimeFormat.HTTP_DATE_TIME, True),
        (1480809600, DateTimeFormat.UNIX_DATE_TIME, True),
        ('1994-11-06T08:49:37', DateTimeFormat.HTTP_DATE_TIME, False),
        (1480809600, DateTimeFormat.HTTP_DATE_TIME, False),
        ('Sun, 06 Nov 1994 03:49:37 GMT', DateTimeFormat.RFC3339_DATE_TIME, False),
        (1480809600, DateTimeFormat.RFC3339_DATE_TIME, False),
        ('1994-11-06T08:49:37', DateTimeFormat.UNIX_DATE_TIME, False),
        ('Sun, 06 Nov 1994 03:49:37 GMT', DateTimeFormat.UNIX_DATE_TIME, False),
        (None, None, False)
    ])
    def test_is_valid_datetime(self, input_dt, input_datetime_format, expected_output):
        actual_output = DateTimeHelper.validate_datetime(input_dt, input_datetime_format)
        assert actual_output == expected_output

    @pytest.mark.parametrize('input_date, expected_output', [
        ('1994-11-06', True),
        (date(1994, 11, 6), True),
        (date(94, 11, 6), True),
        ('1994/11/06', False),
        ('19941106', False),
        ('941106', False),
        ('1941106', False),
        ('1994=11=06', False),
        (123, False)
    ])
    def test_is_valid_date(self, input_date, expected_output):
        actual_output = DateTimeHelper.validate_date(input_date)
        assert actual_output == expected_output




