from ipaddress import ip_address


def is_ip_v4(target):
    try:
        ip_address(target)
    except ValueError:
        return False
    else:
        return True

def format_datetime(dt):
    return dt.strftime("%d %B %Y %I:%M:%S %p")