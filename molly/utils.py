from ipaddress import ip_address


def is_ip_v4(target):
    try:
        ip_address(target)
    except Exception:
        return False
    else:
        return True
