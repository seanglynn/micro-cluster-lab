import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
import logging

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


# crud operations

# Retrieve all users present in the database
async def retrieve_users():
    users = []
    async for user in results_collection.find():
        user_fmt=user_helper(user)
        print(user_fmt)
        users.append(user_fmt)
    return users


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
            '$gte':'{}'.format(ts_start),
            '$lte':'{}'.format(ts_end)
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
