import os
from pyrogram import Client, filters
from pyrogram.types import Message
from MonarchX import MonarchX
from config import HANDLER
from .help import add_command_help


@MonarchX.on_message(filters.command("msave", HANDLER) & filters.me)
async def msave(client: Client, message: Message):
    media = message.reply_to_message.media

    if not media:
        await message.edit("<b>Media is required</b>")
        return
    await message.delete()

    try:
        path = await message.reply_to_message.download()
    except Exception as e:
        await message.reply(f"Error downloading media: {str(e)}")
        return

    # Check the media type and send it accordingly
    if media.type == "photo":
        try:
            await client.send_photo("me", path)
        except Exception as e:
            await message.reply(f"Error sending photo: {str(e)}")
    elif media.type == "video":
        try:
            await client.send_video("me", path)
        except Exception as e:
            await message.reply(f"Error sending video: {str(e)}")
    elif media.type == "document":
        try:
            await client.send_document("me", path)
        except Exception as e:
            await message.reply(f"Error sending document: {str(e)}")

    os.remove(path)

add_command_help(
    "msave",
    [
        ["msave", "Save media files (photo, video, document) to your saved messages."],
    ]
)