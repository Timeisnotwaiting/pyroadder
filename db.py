from motor.motor_asyncio import AsyncIOMotorClient as MongoClient


import config



mongo = MongoClient(config.MONGO_DB_URL)
db = mongo.PSDB

scrdb = db.scr

async def add(a: int):
    found = scrdb.find_one({"a": a})
    if not found:
        return await scrdb.insert_one({"a": a})
    

async def pop(a: int):
    found = scrdb.find_one({"a": a})
    if found:
        return await scrdb.delete_one({"a": a})

async def target():
    users = scrdb.find({"a": {"$gt": 0}})
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list
