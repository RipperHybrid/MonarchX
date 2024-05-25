from MonarchX import db
import asyncio

collection_pmguard = db["pmguard"]
collection_users = db["approved_users"]
collection_pm_messages = db["pm_messages"]
collection_block_messages = db["block_messages"]

PMPERMIT_MESSAGE = (
    "`Ok! Stop Right there Read this first before sending any new messages.\n\n`"
    "`I'm a bot Protecting this user's PM from any kind of Spam.`"
    "`Please wait for my Master to come back Online.\n\n`"
    "`Until then, Don't spam, Or you'll get blocked and reported!`"
)

BLOCKED = "`Guess You're A Spammer, [{name}](tg://user?id={user_id}). Blocked Successfully.`"

LIMIT = 5

async def set_pm(value: bool):
    doc = {"_id": 1, "pmpermit": value}
    await collection_pmguard.update_one({"_id": 1}, {"$set": {"pmpermit": value}}, upsert=True)

async def set_permit_message(text):
    await collection_pm_messages.update_one({"_id": 1}, {"$set": {"pmpermit_message": text}}, upsert=True)

async def set_block_message(text):
    await collection_block_messages.update_one({"_id": 1}, {"$set": {"block_message": text}}, upsert=True)

async def set_limit(limit):
    await collection_pmguard.update_one({"_id": 1}, {"$set": {"limit": limit}}, upsert=True)

async def get_pm_settings():
    result = await collection_pmguard.find_one({"_id": 1})
    if not result:
        pmpermit = False
        pm_message = PMPERMIT_MESSAGE
        block_message = BLOCKED
        limit = LIMIT
    else:
        pmpermit = result.get("pmpermit", False)
        pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
        block_message = result.get("block_message", BLOCKED)
        limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message

async def allow_user(chat):
    await collection_users.update_one({"_id": "Approved"}, {"$addToSet": {"users": chat}}, upsert=True)

async def get_approved_users():
    results = await collection_users.find_one({"_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []

async def deny_user(chat):
    await collection_users.update_one({"_id": "Approved"}, {"$pull": {"users": chat}})

async def pm_guard():
    result = await collection_pmguard.find_one({"_id": 1})
    if not result:
        return False
    if not result.get("pmpermit", False):
        return False
    else:
        return True

async def clear_all_db():
    await collection_pmguard.delete_many({})
    await collection_users.delete_many({})
    await collection_pm_messages.delete_many({})
    await collection_block_messages.delete_many({})
