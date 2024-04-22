import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import HANDLER as cmd
from MonarchX.helpers.tools import get_arg
from .help import add_command_help

@Client.on_message(filters.me & filters.command(["dw"], cmd))
async def download_media(client: Client, message: Message):
    args = get_arg(message)
    if not message.reply_to_message and not args:
        return await message.edit("**Please Reply to a Message Containing the Media**")
    
    # Default timeout value
    timeout_value = 100

    # Check if user specified custom timeout
    if args:
        try:
            timeout_value = int(args)
        except ValueError:
            return await message.edit("**Invalid timeout value. Please provide a valid integer value in seconds.**")
    
    bot = "UVDownloaderBot"
    channel_link = "https://t.me/UVDownloaderNews"
    if message.reply_to_message:
        await message.edit("`Downloading Media . . .`")
        await client.unblock_user(bot)
        await message.reply_to_message.forward(bot)
        
        # Get the current time to track elapsed time
        start_time = asyncio.get_event_loop().time()
        
        # Variable to track if the media has been found
        media_found = False
        while asyncio.get_event_loop().time() - start_time < timeout_value:
            try:
                async for downloaded_media in client.search_messages(bot, limit=1):
                    if downloaded_media and (downloaded_media.video or downloaded_media.photo):
                        await message.delete()
                        if downloaded_media.video:
                            await message.reply_video(
                                video=downloaded_media.video.file_id,
                                reply_to_message_id=message.reply_to_message.id
                                if message.reply_to_message
                                else None,
                            )
                        elif downloaded_media.photo:
                            await message.reply_photo(
                                photo=downloaded_media.photo.file_id,
                                reply_to_message_id=message.reply_to_message.id
                                if message.reply_to_message
                                else None,
                            )
                        media_found = True
                        break
                    elif downloaded_media.text and "❗ Unable to download requested content." in downloaded_media.text:
                        await message.edit("❗ Unable to download requested content.")
                        return
            except Exception as e:
                await message.edit(f"An error occurred: {str(e)}")
                return
                
            # If media is found, exit the loop
            if media_found:
                break
            
            # Wait a short duration before checking again
            await asyncio.sleep(1)

        # Check if media was found or if timeout occurred
        if not media_found:
            await message.edit(f"**Failed to download the media within {timeout_value} seconds. Please check if you have joined the [channel]({channel_link}) to download the media.**", disable_web_page_preview=True)

add_command_help(
    "download",
    [
        [
            f"dw or dw [timeout]",
            "Downloads a video or photo from the replied message with an optional custom timeout in seconds. Default timeout is 100 seconds.",
        ],
    ],
)