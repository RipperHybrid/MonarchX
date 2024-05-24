from pyrogram import Client, filters
from pyrogram.types import Message
from .help import add_command_help
from config import HANDLER
from MonarchX.MonarchX_db.blocklist_db import (
    get_blacklisted_stickers,
    get_blocklist_warns,
    add_to_blocklist,
    remove_from_blocklist,
    clear_blocklist,
    BLOCKLIST_WARN_MESSAGE,
    BLOCKLIST_BLOCKED_MESSAGE,
    set_blocklist_warns,
    set_blocklist_warns_limit,
    get_blocklist_warns_limit,
    set_blocklist_mode,
    get_blocklist_mode,
    toggle_blocklist
)

WARN_LIMIT = 3

@Client.on_message(
    filters.private
    & filters.incoming
    & filters.sticker
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def handle_blacklisted_stickers(client, message):
    print("Received a message with a sticker")

    sticker_unique_id = message.sticker.file_unique_id if message.sticker else None
    print(f"Sticker Unique ID: {sticker_unique_id}")

    if not sticker_unique_id:
        print("No sticker unique ID found")
        return

    blacklisted_stickers = await get_blacklisted_stickers()
    print("Blacklisted stickers:", blacklisted_stickers)

    if sticker_unique_id in blacklisted_stickers:
        print("Sticker is blacklisted")

        user_id = message.from_user.id
        print("User ID:", user_id)

        user_warns = await get_blocklist_warns(user_id)
        print(f"User {user_id} warns: {user_warns}")

        mode = await get_blocklist_mode()
        if mode == "warn":
            warn_limit = await get_blocklist_warns_limit()
            if user_warns >= warn_limit:
                print("User has exceeded the warning limit")
                await message.delete()
                await client.block_user(user_id)
                await message.reply_text(BLOCKLIST_BLOCKED_MESSAGE)
                print("User blocked")
                return

            await message.delete()
            await message.reply_text(BLOCKLIST_WARN_MESSAGE)
            await set_blocklist_warns(user_id, user_warns + 1)
            print(f"Warning message sent, user {user_id} warns updated to {user_warns + 1}")
        elif mode == "del":
            await message.delete()
            await message.reply_text("This sticker is blacklisted. Please refrain from using it.")
    else:
        print(f"Sticker {sticker_unique_id} is not blacklisted")

@Client.on_message(filters.command("blacklistmode", HANDLER) & filters.me)
async def set_blocklist_mode_command(client: Client, message: Message):
    if len(message.command) == 2:
        mode = message.command[1].lower()
        if mode == "del" or mode == "warn":
            await set_blocklist_mode(mode)
            await message.edit_text(f"Blacklist mode set to '{mode}'.")
            return

    await message.edit_text("Invalid command format. Use: /blacklistmode [del | warn]")

@Client.on_message(filters.command("setwarn", HANDLER) & filters.me)
async def set_warn_limit_command(client: Client, message: Message):
    if len(message.command) == 2 and message.command[1].isdigit():
        warn_limit = int(message.command[1])
        await set_blocklist_warns_limit(warn_limit)
        await message.edit_text(f"Warn limit set to {warn_limit}.")
    else:
        await message.edit_text("Invalid command format. Use: /setwarn <warn_limit>")

@Client.on_message(filters.command("toggleblacklist", HANDLER) & filters.me)
async def toggle_blacklist_command(client: Client, message: Message):
    state = await toggle_blocklist()
    if state:
        await message.edit_text("Blacklist is now enabled.")
    else:
        await message.edit_text("Blacklist is now disabled.")

@Client.on_message(filters.command("addblocklist", HANDLER) & filters.me)
async def add_blocklist_command(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.sticker:
        sticker_unique_id = message.reply_to_message.sticker.file_unique_id
        blacklisted_stickers = await get_blacklisted_stickers()
        if sticker_unique_id not in blacklisted_stickers:
            await add_to_blocklist(sticker_unique_id)
            await message.edit_text("Sticker added to blocklist.")
        else:
            await message.edit_text("Sticker already exists in the blocklist.")
    else:
        await message.edit_text("Please reply to a sticker message to add it to the blocklist.")

@Client.on_message(filters.command("rmblocklist", HANDLER) & filters.me)
async def remove_blocklist_command(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.sticker:
        sticker_unique_id = message.reply_to_message.sticker.file_unique_id
        blacklisted_stickers = await get_blacklisted_stickers()
        if sticker_unique_id in blacklisted_stickers:
            await remove_from_blocklist(sticker_unique_id)
            await message.edit_text("Sticker removed from blocklist.")
        else:
            await message.edit_text("Sticker doesn't exist in the blocklist.")
    else:
        await message.edit_text("Please reply to a sticker message to remove it from the blocklist.")

@Client.on_message(filters.command("clearblocklist", HANDLER) & filters.me)
async def clear_blocklist_command(client: Client, message: Message):
    await clear_blocklist()
    await message.edit_text("Blocklist cleared successfully.")

@Client.on_message(filters.command("blacklisted", HANDLER) & filters.me)
async def list_blacklisted_command(client: Client, message: Message):
    blacklisted_stickers = await get_blacklisted_stickers()
    if blacklisted_stickers:
        stickers_info = "\n".join(blacklisted_stickers)
        await message.edit_text(f"Blacklisted stickers:\n{stickers_info}")
    else:
        await message.edit_text("No stickers are currently blacklisted.")

add_command_help(
    "blocklist",
    [
        ["addblocklist", "Add the replied sticker to the blocklist."],
        ["rmblocklist", "Remove the replied sticker from the blocklist."],
        ["blacklisted", "List all stickers currently blacklisted."],
        ["clearblocklist", "Clear all stickers from the blocklist."],
        ["toggleblacklist", "Toggle the blacklist on and off."],
        ["blacklistmode [del | warn]", "Set the mode for blacklisted stickers. Modes: del (delete sticker) or warn (warn user)."],
        ["setwarn <warn_limit>", "Set the warn limit for blacklisted stickers."],
    ]
)
