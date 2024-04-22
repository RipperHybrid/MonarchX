import asyncio
from pyrogram import Client, filters
from pyrogram.errors import YouBlockedUser
from pyrogram.types import Message
from MonarchX.utils.tools import extract_user
from .help import add_command_help

@Client.on_message(filters.command(["sg", "sa", "sangmata"], ".") & filters.me)
async def sg(client: Client, message: Message):
    args = await extract_user(message)
    processing_msg = await message.edit_text("Processing...")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await processing_msg.edit("Please specify a valid user.")
    bot_username = "SangMata_BOT"
    try:
        await client.send_message(bot_username, f"allhistory {user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot_username)
        await client.send_message(bot_username, f"allhistory {user.id}")
    await asyncio.sleep(1)

    async for stalk in client.search_messages(bot_username, query="Name", limit=1):
        if not stalk:
            await message.edit_text("**This person has never changed their name.**")
            return
        elif stalk:
            await message.edit(stalk.text)
            await stalk.delete()

    async for stalk in client.search_messages(bot_username, query="Username", limit=1):
        if stalk:
            await message.reply(stalk.text)
            await stalk.delete()

add_command_help(
    "sangmata",
    [
        ["sg", "Query a user its names and usernames in all groups."],
    ]
)