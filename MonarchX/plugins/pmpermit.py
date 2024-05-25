from pyrogram import filters
import asyncio
from MonarchX import MonarchX 
from MonarchX.helpers.help_func import get_arg, denied_users
import MonarchX.MonarchX_db.pm_db as Zectdb
from config import HANDLER, OWNER_ID
from .help import add_command_help

FLOOD_CTRL = 0
ALLOWED = []
USERS_AND_WARNS = {}

@MonarchX.on_message(filters.command("pmguard", HANDLER) & filters.me)
async def pmguard(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**I only understand on or off**")
        return
    if arg == "off":
        await Zectdb.set_pm(False)
        await message.edit("**PM Guard Deactivated**")
    if arg == "on":
        await Zectdb.set_pm(True)
        await message.edit("**PM Guard Activated**")

@MonarchX.on_message(filters.command("setlimit", HANDLER) & filters.me)
async def setlimit(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Set limit to what?**")
        return
    await Zectdb.set_limit(int(arg))
    await message.edit(f"**Limit set to {arg}**")

@MonarchX.on_message(filters.command("setpmmsg", HANDLER) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**What message to set**")
        return
    if arg == "default":
        await Zectdb.set_permit_message(Zectdb.PMPERMIT_MESSAGE)
        await message.edit("**Anti_PM message set to default**.")
        return
    await Zectdb.set_permit_message(f"`{arg}`")
    await message.edit("**Custom anti-pm message set**")

@MonarchX.on_message(filters.command("setblockmsg", HANDLER) & filters.me)
async def setblockmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**What message to set**")
        return
    if arg == "default":
        await Zectdb.set_block_message(Zectdb.BLOCKED)
        await message.edit("**Block message set to default**.")
        return
    await Zectdb.set_block_message(f"`{arg}`")
    await message.edit("**Custom block message set**")

@MonarchX.on_message(filters.command("allow", HANDLER) & filters.me & filters.private)
async def allow(client, message):
    chat_id = message.chat.id
    pmpermit, pm_message, limit, block_message = await Zectdb.get_pm_settings()
    await Zectdb.allow_user(chat_id)
    user_info = await client.get_users(chat_id)
    first_name = user_info.first_name
    await message.edit(f"**I have allowed [{first_name}](tg://user?id={chat_id}) to PM me.**")
    async for message in MonarchX.search_messages(
        chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
    ):
        await message.delete()
    USERS_AND_WARNS.update({chat_id: 0})

@MonarchX.on_message(filters.command("deny", HANDLER) & filters.me & filters.private)
async def deny(client, message):
    chat_id = message.chat.id
    await Zectdb.deny_user(chat_id)
    user_info = await client.get_users(chat_id)
    first_name = user_info.first_name
    await message.edit(f"**I have denied [{first_name}](tg://user?id={chat_id}) to PM me.**")

@MonarchX.on_message(
    filters.private
    & filters.create(denied_users)
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def reply_pm(client, message):
    global FLOOD_CTRL
    pmpermit, pm_message, limit, block_message = await Zectdb.get_pm_settings()
    user = message.from_user.id
    user_warns = 0 if user not in USERS_AND_WARNS else USERS_AND_WARNS[user]
    if user_warns <= limit - 2:
        user_warns += 1
        USERS_AND_WARNS.update({user: user_warns})
        if not FLOOD_CTRL > 0:
            FLOOD_CTRL += 1
        else:
            FLOOD_CTRL = 0
            return
        await message.reply(pm_message, disable_web_page_preview=True)
        return
    user_info = await client.get_users(user)
    first_name = user_info.first_name
    custom_block_message = block_message.format(name=first_name)
    await message.reply(custom_block_message, disable_web_page_preview=True)
    await client.block_user(message.chat.id)
    USERS_AND_WARNS.update({user: 0})

@MonarchX.on_message(filters.command("cleardb", HANDLER) & filters.me)
async def cleardb(client, message):
    await Zectdb.clear_all_db()
    await message.edit("**All database collections have been cleared.**")

@MonarchX.on_message(filters.command("showallowed", HANDLER) & filters.me)
async def showallowed(client, message):
    users = await Zectdb.get_approved_users()
    user_list = []
    for user_id in users:
        user_info = await client.get_users(user_id)
        first_name = user_info.first_name
        user_link = f"[{first_name}](tg://user?id={user_id})"
        user_list.append(user_link)
    formatted_list = "\n".join(user_list)
    await message.edit(f"**Allowed Users:**\n{formatted_list}")

add_command_help(
    "pmguard",
    [
        ["pmguard", "Activate or deactivate PM Guard."],
        ["setlimit", "Set the limit for warning a user before blocking them."],
        ["setpmmsg", "Set a custom message for permitting PMs."],
        ["setblockmsg", "Set a custom message for blocking PMs."],
        ["allow", "Allow a user to PM the bot."],
        ["deny", "Deny a user from PMing the bot."],
        ["cleardb", "Clear all database collections."],
        ["showallowed", "Show all allowed users."]
    ]
)
