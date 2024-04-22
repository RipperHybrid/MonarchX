import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from config import HANDLER as cmd
from MonarchX.helpers.tools import get_arg

from .help import add_command_help

@Client.on_message(filters.me & filters.command(["q", "quotly"], cmd))
async def quotly(client: Client, message: Message):
    args = get_arg(message)
    if not message.reply_to_message and not args:
        return await message.edit("**Please Reply to a Message**")
    bot = "QuotLyBot"
    if message.reply_to_message:
        await message.edit("`Making a Quote . . .`")
        await client.unblock_user(bot)
        if args:
            await client.send_message(bot, f"/qcolor {args}")
            await asyncio.sleep(1)
        else:
            pass
        await message.reply_to_message.forward(bot)
        timeout = 10  # Adjust timeout as needed
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < timeout:
            try:
                async for quotly in client.search_messages(bot, limit=1):
                    if quotly and quotly.sticker:
                        await message.delete()
                        await message.reply_sticker(
                            sticker=quotly.sticker.file_id,
                            reply_to_message_id=message.reply_to_message.id
                            if message.reply_to_message
                            else None,
                        )
                        return  # Exit the function once the quotly sticker is found
            except asyncio.TimeoutError:
                pass  # Continue the loop if there's a timeout
            await asyncio.sleep(1)  # Wait before checking again
        await message.edit("**Timeout: Failed to create Quotly Sticker**")

add_command_help(
    "quotly",
    [
        [
            f"q or quotly",
            "Converts a message into a sticker with a random background.",
        ],
        [
            f"q <color> or quotly <color>",
            "Converts a message into a sticker with a custom background color.",
        ],
    ],
)