from datetime import datetime, timezone


# Get the current UTC time
def get_now_utc():
    return datetime.now(timezone.utc)
