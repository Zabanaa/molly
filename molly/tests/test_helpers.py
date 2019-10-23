import datetime
from molly.utils import (
    is_ip_v4,
    format_datetime
)


def test_is_ip_v4():
    is_ip = is_ip_v4('127.0.0.1')
    assert is_ip == True


def test_is_not_ip_v4():
    is_ip = is_ip_v4('localhost')
    assert is_ip == False


def test_format_datetime():
    test_dt = datetime.datetime(2019, 10, 23, 16, 18, 57, 688789)
    fmt_datetime = format_datetime(test_dt)
    assert fmt_datetime == '23 October 2019 04:18:57 PM'