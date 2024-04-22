from pyrogram import filters,enums
from pyrogram.types import Message

from MonarchX import MonarchX
from requests import get
import datetime
import config
from MonarchX.helpers.help_func import make_carbon
import os
from config import HANDLER,OWNER_ID
import asyncio
import requests
import yt_dlp
from youtube_search import YoutubeSearch
from .help import add_command_help



import httpx

timeout = httpx.Timeout(40, pool=None)
http = httpx.AsyncClient(http2=True, timeout=timeout)
weather_apikey = "8de2d8b3a93542c9a2d8b3a935a2c909"
get_coords = "https://api.weather.com/v3/location/search"
url = "https://api.weather.com/v3/aggcommon/v3-wx-observations-current"
headers = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2012K11AG Build/SQ1D.211205.017)"
}


@MonarchX.on_message(filters.command("song",prefixes=HANDLER) & filters.me)
def download_song(_, message):
    query = " ".join(message.command[1:])  
    print(query)
    m = message.reply_text("**🔍**")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("**⚠️ No results were found. Make sure you typed the information correctly**")
        print(str(e))
        return
    m.edit("**Downloading .. Your Request song**")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("**💀 Uploading ..**")
        try:
            message.delete()
        except:
            pass

        message.reply_audio(
            audio_file,
            thumb=thumb_name,
            title=title,
            caption=f"{title}\n**Uploaded by {message.from_user.mention}**",
            duration=dur
        )
        m.delete()
    except Exception as e:
        m.edit(" - An error check logs again sor!!")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

@MonarchX.on_message(filters.command("weather",prefixes=HANDLER) & filters.me)
async def weather(_, m: Message):
    if len(m.command) == 1:
        return await m.reply_text(
            "<b>ᴜsᴀɢᴇ:</b> <code>/weather location ᴏʀ city</code> - ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴡᴇᴀᴛʜᴇʀ ɪɴ <i>ʟᴏᴄᴀᴛɪᴏɴ ᴏʀ ᴄɪᴛʏ</i>"
        )
    msg = await m.reply_text("Getting Weather info...")

    r = await http.get(
        get_coords,
        headers=headers,
        params=dict(
            apiKey=weather_apikey,
            format="json",
            language="en",
            query=m.text.split(maxsplit=1)[1],
        ),
    )
    loc_json = r.json()
    try:
        await m.delete()
    except:
        return

    if not loc_json.get("location"):
        await msg.edit("ʟᴏᴄᴀᴛɪᴏɴ ɴᴏᴛ ғᴏᴜɴᴅ")
    else:
        pos = f"{loc_json['location']['latitude'][0]},{loc_json['location']['longitude'][0]}"
        r = await http.get(
            url,
            headers=headers,
            params=dict(
                apiKey=weather_apikey,
                format="json",
                language="en",
                geocode=pos,
                units="m",
            ),
        )
        res_json = r.json()

        obs_dict = res_json["v3-wx-observations-current"]

        res = "<b>{location}</b>:\n\nᴛᴇᴍᴘᴇʀᴀᴛᴜʀᴇ: <code>{temperature} °C</code>\nᴛᴇᴍᴘᴇʀᴀᴛᴜʀᴇ ғᴇᴇʟs ʟɪᴋᴇ: <code>{feels_like} °C</code>\nᴀɪʀ ʜᴜᴍɪᴅɪᴛʏ: <code>{air_humidity}%</code>\nᴡɪɴᴅ sᴘᴇᴇᴅ: <code>{wind_speed} km/h</code>\n\n- <i>{overview}</i>".format(
            location=loc_json["location"]["address"][0],
            temperature=obs_dict["temperature"],
            feels_like=obs_dict["temperatureFeelsLike"],
            air_humidity=obs_dict["relativeHumidity"],
            wind_speed=obs_dict["windSpeed"],
            overview=obs_dict["wxPhraseLong"],
        )

        await msg.edit(res)

@MonarchX.on_message(filters.command("carbon", prefixes=HANDLER) & filters.me)
async def carbon(_, m: Message):
    msg = await m.reply_text("Trying...")  # Await here
    if m.reply_to_message:
        if m.reply_to_message.text:
            txt = m.reply_to_message.text
        else:
            return await msg.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ.")
    else:
        try:
            txt = m.text.split(None, 1)[1]
        except IndexError:
            return await msg.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ.")
    m = await msg.edit("ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴀʀʙᴏɴ...")
    carbon = await make_carbon(txt)
    await m.edit("ᴜᴩʟᴏᴀᴅɪɴɢ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴄᴀʀʙᴏɴ...")
    await MonarchX.send_photo(
        m.chat.id,
        photo=carbon,
    )
    await m.delete()
    carbon.close()


async def convert_to_datetime(timestamp): # Unix timestamp
    try:
        date = datetime.datetime.fromtimestamp(timestamp)
        return date
    except Exception as e:
        print(f"Error converting timestamp: {e}")
        return ""

async def spacebin(text: str):
    url = "https://spaceb.in/api/v1/documents/"
    response = requests.post(url, data={"content": text, "extension": "txt"})
    id = response.json().get('payload').get('id')
    res = requests.get(f"https://spaceb.in/api/v1/documents/{id}").json()
    created_at = res.get("payload").get("created_at")
    link = f"https://spaceb.in/{id}"
    raw = f"https://spaceb.in/api/v1/documents/{id}/raw"
    timedate = await convert_to_datetime(created_at)
    string = f"""\u0020
**Here's the link**: **[Paste link]({link})**
**Here's the link**: **[Raw View]({raw})**
**Created datetime**: {timedate}
"""
    return string

@MonarchX.on_message(filters.command("paste", HANDLER) & filters.me)
async def paste(_, message):
    # share your codes on https://spacebin.in
    msg = await message.reply_text("Trying...")  # Added await here
    if not message.reply_to_message:
        try:
            text = message.text.split(None, 1)[1]
        except IndexError:
            await msg.edit("=> Input text to paste else reply.")
            return

        link = await spacebin(text)
        await msg.edit(link, disable_web_page_preview=True)
        return

    elif bool(message.reply_to_message.text or message.reply_to_message.caption):
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        elif message.reply_to_message.caption:
            text = message.reply_to_message.caption

        link = await spacebin(text)
        await msg.edit(link, disable_web_page_preview=True)
        return

    elif (message.reply_to_message.document and bool(message.reply_to_message.document.mime_type.startswith("text/"))):
        try:
            path = await MonarchX.download_media(message.reply_to_message)
            with open(path, "r") as file:
                text = file.read()
            os.remove(path)
            link = await spacebin(text)
            await msg.edit(link, disable_web_page_preview=True)
        except Exception as e:
            print(f"Error processing document: {e}")
            await msg.edit("=> Error processing the document.")
    else:
        await msg.edit("=> I am unable to paste this.")


add_command_help(
    "tools",
    [
        ["song [query]", "Downloads and sends the audio of the provided song query from YouTube."],
        ["weather [location or city]", "Get information about the weather in the provided location or city."],
        ["carbon", "Generates a carbon code image of the replied-to or provided text."],
        ["paste [text]", "Uploads and shares the provided text on Spacebin."],
        ["paste", "Uploads and shares the replied-to text or caption on Spacebin."],
    ]
)