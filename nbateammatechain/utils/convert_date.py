import datetime

def conversion(date):
    try:
        d = datetime.datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")
    except Exception:
        d = None
    return d
