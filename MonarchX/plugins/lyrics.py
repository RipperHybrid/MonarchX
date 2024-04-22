from MonarchX import MonarchX
from config import HANDLER, OWNER_ID
from pyrogram import filters
import asyncio
import os
import io
import lyricsgenius
from .help import add_command_help
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialize the Genius API client with your access token
genius = lyricsgenius.Genius("RSzHN7VttrvX2zH1LE86qnnOP_nPlEuOIpCCgQ2m")

@MonarchX.on_message(filters.command("lyrics", prefixes=HANDLER) & filters.user(OWNER_ID))
async def search_lyrics(_, message):
    if len(message.text.split()) < 2:
        return await message.reply("Master, enter the name of the song to search for its lyrics.")
    MSG = await message.reply("Loading...")
    song_name = " ".join(message.command[1:])
    try:
        # Search for the song lyrics
        song = genius.search_song(song_name)
        if song is None:
            return await MSG.edit("Song is not found.")
        song_txt = f"Lyrics for '{song.title}' by {song.artist}:\n\n{song.lyrics}"
        if len(song_txt) > 3900:
            with io.BytesIO(str.encode(song_txt)) as output:
                output.name = f"{song.title} lyrics.txt"
                await message.reply_document(
                    document=output
                )
                await MSG.delete()
        else:
            await MSG.edit(f"Lyrics for '{song.title}' by {song.artist}:\n\n{song.lyrics}")
    except Exception as e:
        await MSG.edit(f"An error occurred: {e}")

add_command_help(
    "lyrics",
    [
        [f"lyrics [Song Name]", "Get Song Lyrics From Genius Api."],
    ],
)

# API RIGHTS RESERVED TO https://genius.com/
# IF YOU WANT CREATE API GO TO https://genius.com/api-clients AND CREATE
# THANKS FOR READING
