import datetime
import motor.motor_asyncio
from config import MONGO_URL, MONGO_DB_NAME, MONGO_COLLECTION
from collections import defaultdict


async def get_period_stat(dt_from: datetime.datetime, dt_upto: datetime.datetime, group_type: str) -> str:
    # Connect to MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION]
    
    all_times = []
    if group_type == "month":
        d = dt_from
        d = d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        while d <= dt_upto:
            if d >= dt_from:
                all_times.append(d)
            # goto next month
            d += datetime.timedelta(days=32)
            d = d.replace(day=1)
    elif group_type == "day":
        d = dt_from
        d = d.replace(hour=0, minute=0, second=0, microsecond=0)
        while d <= dt_upto:
            if d >= dt_from:
                all_times.append(d)
            d += datetime.timedelta(days=1)
    elif group_type == "hour":
        d = dt_from
        d = d.replace(minute=0, second=0, microsecond=0)
        while d <= dt_upto:
            if d >= dt_from:
                all_times.append(d)
            d += datetime.timedelta(hours=1)        
            
    # Match condition
    match_condition = {
        "dt": {"$gte": dt_from, "$lte": dt_upto}
    }

    # Group by condition
    if group_type == "month":
        group_by = {
            "_id": {
                "year": {"$year": "$dt"},
                "month": {"$month": "$dt"}
            },
            "total": {"$sum": "$value"}
        }
    elif group_type == "day":
        group_by = {
            "_id": {
                "year": {"$year": "$dt"},
                "month": {"$month": "$dt"},
                "day": {"$dayOfMonth": "$dt"}
            },
            "total": {"$sum": "$value"}
        }
    elif group_type == "hour":
        group_by = {
            "_id": {
                "year": {"$year": "$dt"},
                "month": {"$month": "$dt"},
                "day": {"$dayOfMonth": "$dt"},
                "hour": {"$hour": "$dt"}
            },
            "total": {"$sum": "$value"}
        }
    else:
        raise ValueError(group_type)
    dataset = []
    labels = []
    
    dataset_as_dict = defaultdict(int)
    
    # Perform aggregation
    async for result in collection.aggregate([{"$match": match_condition}, {"$group": group_by}, {"$sort": {"_id": 1}}]):
        d = datetime.datetime(
            year=result["_id"]["year"],
            month=result["_id"].get("month", 1),
            day=result["_id"].get("day", 1),
            hour=result["_id"].get("hour", 0)
        )
        dataset_as_dict[d] = result["total"]
    
    for d in all_times:
        dataset.append(dataset_as_dict[d])
        labels.append(d.strftime("%Y-%m-%dT%H:%M:%S"))
        
    return {
        "dataset": dataset,
        "labels": labels,
    }
