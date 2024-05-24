from MonarchX import db
import asyncio

blocklist_collection = db["blocklist"]
blocklist_warn_collection = db["blocklist_warn"]
blocklist_mode_collection = db["blocklist_mode"]

BLOCKLIST_WARN_MESSAGE = "You have been warned for using a blacklisted sticker."
BLOCKLIST_BLOCKED_MESSAGE = "You have been blocked for repeatedly using blacklisted stickers."

async def add_to_blocklist(sticker_unique_id):
    doc = {"_id": sticker_unique_id}
    await blocklist_collection.insert_one(doc)
    print(f"Added to blocklist: {sticker_unique_id}")

async def remove_from_blocklist(sticker_unique_id):
    await blocklist_collection.delete_one({"_id": sticker_unique_id})
    print(f"Removed from blocklist: {sticker_unique_id}")

async def get_blacklisted_stickers():
    result = await blocklist_collection.find().to_list(length=None)
    blacklisted_stickers = [sticker["_id"] for sticker in result]
    print(f"Retrieved blacklisted stickers: {blacklisted_stickers}")
    return blacklisted_stickers

async def clear_blocklist():
    await blocklist_collection.delete_many({})
    print("Cleared blocklist")

async def get_blocklist_warns(user_id):
    result = await blocklist_warn_collection.find_one({"_id": user_id})
    warns = result.get("warns", 0) if result else 0
    print(f"User {user_id} has {warns} warns")
    return warns

async def set_blocklist_warns(user_id, warn_count):
    doc = {"_id": user_id, "warns": warn_count}
    await blocklist_warn_collection.update_one({"_id": user_id}, {"$set": doc}, upsert=True)
    print(f"Set warns for user {user_id} to {warn_count}")

async def set_blocklist_warns_limit(warn_limit):
    doc = {"_id": "warn_limit", "limit": warn_limit}
    await blocklist_warn_collection.update_one({"_id": "warn_limit"}, {"$set": doc}, upsert=True)
    print(f"Set warn limit to {warn_limit}")

async def get_blocklist_warns_limit():
    result = await blocklist_warn_collection.find_one({"_id": "warn_limit"})
    limit = result.get("limit", 3) if result else 3
    print(f"Retrieved warn limit: {limit}")
    return limit

async def set_blocklist_mode(mode):
    doc = {"_id": "blocklist_mode", "mode": mode}
    await blocklist_mode_collection.update_one({"_id": "blocklist_mode"}, {"$set": doc}, upsert=True)
    print(f"Set blocklist mode to {mode}")

async def get_blocklist_mode():
    result = await blocklist_mode_collection.find_one({"_id": "blocklist_mode"})
    mode = result.get("mode") if result else None
    print(f"Retrieved blocklist mode: {mode}")
    return mode

async def toggle_blocklist():
    current_mode = await get_blocklist_mode()
    new_mode = "off" if current_mode == "on" else "on"
    await set_blocklist_mode(new_mode)
    print(f"Toggled blocklist to {new_mode}")
