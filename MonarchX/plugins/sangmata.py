import asyncio
from pyrogram import Client, filters
from pyrogram.errors import YouBlockedUser
from pyrogram.types import Message
from MonarchX.utils.tools import extract_user
from .help import add_command_help
from config import HANDLER

@Client.on_message(filters.command(["sg", "sa", "sangmata"], HANDLER) & filters.me)
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

    async def handle_response():
        found_data = False

        async for msg in client.get_chat_history(bot_username, limit=10):
            if "History for" in msg.text:
                await processing_msg.edit_text(msg.text)
                found_data = True
                break
            elif "No data available" in msg.text:
                user_link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                await processing_msg.edit_text(f"No information available about {user_link}")
                found_data = True
                break
            elif "Sorry, you have used up your quota for today." in msg.text:
                await processing_msg.edit_text("Daily quota reached. Please try again tomorrow.")
                found_data = True
                break

        if not found_data:
            await processing_msg.edit_text("Failed to retrieve information. Please try again.")

    await handle_response()

add_command_help(
    "sangmata",
    [
        ["sg", "Query a user its names and usernames in all groups."],
    ]
)
