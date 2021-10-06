import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
import logging
from datetime import datetime

MONGO_DETAILS = config('MONGO_DETAILS') # read environment variable.

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.yieldify
results_collection = database.get_collection("results")


# helpers
def user_helper(user) -> dict:
    result={
        "id": str(user["_id"]),
        "timestamp": user["timestamp"],
        "user_id": user["user_id"],
        "url": user["url"],
        "ip": user["ip"],
        "browser": user["browser"],
        "os": user["os"],
        "city_name": user["city_name"],
        "country_name": user["country_name"],
    }
    return result

##CRUD
# Retrieve all users present in the database
async def retrieve_users():
    users = []
    async for user in results_collection.find():
        user_fmt=user_helper(user)
        print(user_fmt)
        users.append(user_fmt)
    return users


# Calculate percentage of field
async def mongoql_calculate_percentage(field):

    nums = await results_collection.count_documents({})
    stats_result = results_collection.aggregate(
    [
       {
         "$group" : {
            "_id" : f"${field}",
            "count": { "$sum": 1 }
         }
       },
       { "$project": { 
            "count": 1, 
            "percentage": { 
                "$concat": [ { "$substr": [ { "$multiply": [ { "$divide": [ "$count", {"$literal": nums }] }, 100 ] }, 0,2 ] }, "", "%" ]}
            }
       }
    ]
    )
    return stats_result


# Retrieve os %
async def retrieve_os_stats():
    os_percentages = []
    percent_stats = await mongoql_calculate_percentage("os")
    async for os_percent in percent_stats:
        os_percentages.append(os_percent)
    return os_percentages

# Retrieve browser %
async def retrieve_browser_stats():
    browser_percentages = []
    percent_stats = await mongoql_calculate_percentage("browser")
    async for browser_percent in percent_stats:
        browser_percentages.append(browser_percent)
    return browser_percentages


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = await results_collection.insert_one(user_data)
    new_user = await results_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Retrieve a user with a matching ID
async def retrieve_user(id: str) -> dict:
    print(f"retrieve_user: {id}")
    print(id) 
    users = []
    cursor = results_collection.find({"user_id": id})
    for document in await cursor.to_list(length=100):
        if document:
            users.append(user_helper(document))
    return users




# Retrieve a user between two timestamps
async def retrieve_users_ts(ts_start: str, ts_end: str) -> dict:
    print(ts_start)
    print(ts_end)
    users_ts = []
    cursor = await results_collection.find({
        'timestamp':{
            '$gte': ts_start,
            '$lte': ts_end
        }
    })
    for document in await cursor.to_list(length=100):
        if document:
            users_ts.append(user_helper(document))

    
    return users_ts


# Update a user with a matching ID
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await results_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await results_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a user from the database
async def delete_user(id: str):
    user = await results_collection.find_one({"_id": ObjectId(id)})
    if user:
        await results_collection.delete_one({"_id": ObjectId(id)})
        return True
