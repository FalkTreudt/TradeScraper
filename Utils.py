from datetime import datetime, timedelta

def get_last_5_trading_days(today=None):
    if today is None:
        today = datetime.today()

    trading_days = []
    current = today

    while len(trading_days) < 5:
        if current.weekday() < 5:  # Montag–Freitag
            trading_days.insert(0, current.replace(hour=0, minute=0, second=0, microsecond=0))
        current -= timedelta(days=1)

    return trading_days
