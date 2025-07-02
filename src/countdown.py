from datetime import datetime

def get_countdown_string(target_dt):
    now = datetime.now()
    diff = target_dt - now
    if diff.total_seconds() < 0:
        return "The date/time has already passed!"
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s left"
