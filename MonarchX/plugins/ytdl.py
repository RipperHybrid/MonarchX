import asyncio
import requests
import wget
import yt_dlp
import config
import os

from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from .help import add_command_help

from pyrogram import filters
from pyrogram.types import *

from MonarchX import MonarchX, MODULE
from config import HANDLER, OWNER_ID, MONARCHX

@MonarchX.on_message(filters.command("video",prefixes=HANDLER) & filters.me)
async def vsong(client, message):
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        me = await MonarchX.get_me()
        msg = await message.reply("**Getting Video**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **Error:** {e}")
    preview = wget.download(thumbnail)
    await msg.edit("**Process Complete.\n Now Uploading 🌝**")
    await msg.delete()
    try:
        await message.delete()
    except:
        pass
    title = ytdl_data["title"]
    await message.reply_video(file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=f"{title}\n**Uploaded by {message.from_user.mention}**")
    try:
        os.remove(file_name)
    except Exception as e:
        print(e)                                  

flex = {}
chat_watcher_group = 3

                       
ydl_opts = {
    "format": "best",
    "keepvideo": True,
    "prefer_ffmpeg": False,
    "geo_bypass": True,
    "outtmpl": "%(title)s.%(ext)s",
    "quite": True,
}        



__mod_name__ = "UTHOOB"  
    
__help__ = """  
- song: get a song from yt
- video: get video from yt
"""  
    
    
string = {"module": __mod_name__, "help": __help__}   
MODULE.append(string)

add_command_help(
    "ytdl",
    [
        ["song", "Get video from yt."],
        ["video", "Get video from yt."],
    ]
)