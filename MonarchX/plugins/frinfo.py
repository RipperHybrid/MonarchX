from pyrogram import filters
from MonarchX import MonarchX as userbot
from config import HANDLER, OWNER_ID
from .help import add_command_help

@userbot.on_message(filters.me & filters.command(["fi"], prefixes=HANDLER))
async def forward_info(_, message):
    if not message.reply_to_message:
        return await message.edit("`Please reply to a message to get information about the original chat or sender.`")

    original_chat_info = ""

    if message.reply_to_message.forward_from_chat:
        forward_from_chat = message.reply_to_message.forward_from_chat
        original_chat_title = forward_from_chat.title if hasattr(forward_from_chat, "title") else "Unknown"
        original_chat_id = forward_from_chat.id if hasattr(forward_from_chat, "id") else "Unknown"
        original_chat_username = forward_from_chat.username if hasattr(forward_from_chat, "username") else "Not available"

        original_chat_info = (
            f"Original Chat Title: {original_chat_title}\n"
            f"Original Chat ID: {original_chat_id}\n"
            f"Original Chat Username: @{original_chat_username}"
        )
    elif message.reply_to_message.forward_sender_name:
        forward_sender_name = message.reply_to_message.forward_sender_name
        original_chat_info = f"Forward Sender Name: {forward_sender_name}"
    elif message.reply_to_message.forward_from:
        forward_from = message.reply_to_message.forward_from
        forward_from_username = forward_from.username if hasattr(forward_from, "username") else "Not available"
        forward_from_info = (
            f"Forward From User ID: {forward_from.id}\n"
            f"Forward From Username: @{forward_from_username}\n"
            f"Forward From First Name: {forward_from.first_name}"
        )
        original_chat_info = f"Forward From:\n{forward_from_info}"
    elif message.reply_to_message.forward_date:
        forward_date = message.reply_to_message.forward_date
        original_chat_info = f"Forward Date: {forward_date}"
    elif message.reply_to_message.forward_signature:
        forward_signature = message.reply_to_message.forward_signature
        original_chat_info = f"Forward Signature: {forward_signature}"

    await message.edit(original_chat_info)

add_command_help(
    "fi",
    [
        ["fi", "Retrieve information about the original chat or sender of a replied or forwarded message."],
    ]
)
