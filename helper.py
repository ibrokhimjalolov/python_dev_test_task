import datetime


async def get_period_stat(dt_from: datetime.datetime, dt_upto: datetime.datetime, group_type: str) -> str:
    # Here should be your code that calculates statistics
    return f"Period: {dt_from} - {dt_upto}, group type: {group_type}"
