def format_date(value, fmt='%Y-%m-%d'):
    if not value:
        return None
    return value.strftime(fmt)

def format_datetime(value, fmt='%Y-%m-%d %H:%M:%S'):
    if not value:
        return None
    return value.strftime(fmt)