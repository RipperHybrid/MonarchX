import asyncio
import re
import random
import requests
from MonarchX import MonarchX, MODULE
from pyrogram import filters          
from config import OWNER_ID, HANDLER
from .help import add_command_help


@MonarchX.on_message(filters.command("cat", prefixes=HANDLER) & filters.me)
async def cat(_, message):
    api = requests.get("https://api.thecatapi.com/v1/images/search").json()
    url = api[0]["url"]
    if url.endswith(".gif"):
        await message.reply_animation(url)
    else:
        await message.reply_photo(url)

@MonarchX.on_message(filters.regex("baka") & filters.me)
async def baka(_, message):
    reply = message.reply_to_message
    api = requests.get("https://nekos.best/api/v2/baka").json()
    url = api["results"][0]['url']
    anime = api["results"][0]["anime_name"]     
    if reply:
        user = reply.from_user
        name = user.first_name
        username = user.username
        user_profile_link = f"https://t.me/{username}" if username else ""
        user_hyperlink = f"[{name}]({user_profile_link})" if user_profile_link else name
        await reply.reply_animation(url, caption="**• {}**\n**Baka! {}**".format(anime, user_hyperlink))
    else:
        await message.reply_animation(url, caption="**• {}**\n**Baka!**".format(anime))

@MonarchX.on_message(filters.regex("hug") & filters.me)
async def hug(_, message):
    reply = message.reply_to_message
    api = requests.get("https://nekos.best/api/v2/hug").json()
    url = api["results"][0]['url']
    anime = api["results"][0]["anime_name"]     
    if reply:
        user = reply.from_user
        name = user.first_name
        username = user.username
        user_profile_link = f"https://t.me/{username}" if username else ""
        user_hyperlink = f"[{name}]({user_profile_link})" if user_profile_link else name
        await reply.reply_animation(url, caption="**• {}**\n**Hugs! {}**".format(anime, user_hyperlink))
    else:
        await message.reply_animation(url, caption="**• {}**\n**Hugs!**".format(anime))

@MonarchX.on_message(filters.command("in", prefixes=HANDLER) & filters.me)
async def insult(_, message):
    reply = message.reply_to_message
    try:
        insult = requests.get("https://insult.mattbas.org/api/insult").text
        if reply:
            user = reply.from_user
            name = user.first_name
            username = user.username
            user_profile_link = f"https://t.me/{username}" if username else ""
            user_hyperlink = f"[{name}]({user_profile_link})" if user_profile_link else name
            string = insult.replace("You are", user_hyperlink)
            await message.reply(string)
        else:
            await message.reply(insult)
    except Exception as e:
        await message.reply(f"Error: {e}")

@MonarchX.on_message(filters.command("ri", prefixes=HANDLER) & filters.me)
async def riddle(_, message):
    riddle = requests.get("https://riddles-api.vercel.app/random").json()
    question = riddle["riddle"]
    answer = riddle["answer"]
    msg = await message.reply(f"**• Riddle**:\n[ `{question}` ]\n\n[ `The Answer will show automatically 20 seconds after tell me your guess's!` ]")
    await asyncio.sleep(20)
    await msg.edit(f"**• Riddle**:\n[ `{question}` ]\n\n• **Answer**: [ `{answer}` ]")

@MonarchX.on_message(filters.command("qu", prefixes=HANDLER) & filters.me)
async def quote(_, m):
    api = random.choice(requests.get("https://type.fit/api/quotes").json())
    string = api["text"]
    author = api["author"]
    await m.reply(
        f"**Quotes**:\n`{string}`\n\n"
        f"   ~ **{author}**")

@MonarchX.on_message(filters.command("gt", prefixes=HANDLER) & filters.me)
async def google_it(_, message):
    file_id = "CAACAgUAAx0CXss_8QABB0iVY2ZDrB4YHzW6u1xRqKLuUX7b6sEAAhUAA-VDzTc4Ts7oOpk4nx4E"
    if message.reply_to_message:
        await message.reply_to_message.reply_sticker(sticker=file_id, reply_markup=None)
        await message.reply_to_message.reply_text("🔎 [Google](https://www.google.com/search?)", disable_web_page_preview=True)
    else:
        await message.reply_sticker(sticker=file_id, reply_markup=None)
        await message.reply_text("🔎 [Google](https://www.google.com/search?)", disable_web_page_preview=True)


add_command_help(
    "MonarchX",
    [
        ["cat", "Reply with a random cat image or gif."],
        ["baka", "Reply with an anime 'baka' animation."],
        ["hug", "Reply with an anime hug animation."],
        ["in", "Insult someone or yourself."],
        ["ri", "Get a random riddle and its answer."],
        ["qu", "Get a random quote."],
        ["gt", "Reply with a Google sticker and link."],
    ],
)