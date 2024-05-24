from config import HANDLER, OWNER_ID
from MonarchX import MonarchX as app
import os
from pyrogram import filters
from pyrogram.types import User, Message
from pyrogram.errors import PeerIdInvalid
from .help import add_command_help


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


@app.on_message(filters.command("whois", HANDLER) & filters.me)
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await app.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("I don't know that User.")
        return
    common = await app.get_common_chats(user.id)

    await message.reply_text(
        f"**User ID**: `{user.id}`\n"
        f"**First Name**: `{user.first_name}`\n"
        f"**Last Name**: `{user.last_name or ''}`\n"
        f"**Username**: `@{user.username or ''}`\n"
        f"**DC**: `{user.dc_id or '1'}`\n"
        f"**Status**: `{user.status or 'None'}`\n"
        f"**Is Scam**: `{user.is_scam}`\n"
        f"**Is Bot**: `{user.is_bot}`\n"
        f"**Is Verified**: `{user.is_verified}`\n"
        f"**Is Contact**: `{user.is_contact}`\n"
        f"**Total Groups In Common**: `{len(common)}`"
    )


@app.on_message(filters.command("id", HANDLER) & filters.me)
async def id_command(client, message):
    chat_id = message.chat.id
    owner_id = message.from_user.id

    if message.chat.type == "private":
        text = (
            f"👤 UserID: `{owner_id}`\n"
            f"🗿 Owner ID: `{owner_id}`"
        )
    else:
        if message.reply_to_message:
            replied_message = message.reply_to_message
            if replied_message:
                replied_user_id = replied_message.from_user.id
                text = (
                    f"💫 ChatID: `{chat_id}`\n"
                    f"👤 Replied UserID: `{replied_user_id}`\n"
                    f"🗿 Owner ID: `{owner_id}`"
                )
            else:
                text = (
                    f"💫 ChatID: `{chat_id}`\n"
                    f"🗿 Owner ID: `{owner_id}`"
                )
        else:
            text = (
                f"💫 ChatID: `{chat_id}`\n"
                f"🗿 Owner ID: `{owner_id}`"
            )

    try:
        await message.edit_text(text)
    except Exception as e:
        print(f"An error occurred: {e}")
        await message.reply_text("An error occurred while processing the command.")


add_command_help(
    "info",
    [
        ["whois [user_id or username]", "Retrieve information about a user."],
        ["id [user_id or username]", "Retrieve the user ID and chat ID."],
    ]
)
