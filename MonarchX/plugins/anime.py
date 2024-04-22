import requests
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from .help import add_command_help

from config import HANDLER as cmd

BASE_URL = "https://api.waifu.pics"

SFW_CATEGORIES = [
    "waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug", "awoo",
    "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive",
    "handhold", "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke",
    "dance", "cringe"
]

@Client.on_message(filters.command("randomanime", cmd) & filters.me)
async def random_anime(client: Client, message: Message):
    await message.edit("Fetching a random anime image...")

    try:
        image_url = fetch_random_image("sfw", random.choice(SFW_CATEGORIES))

        if image_url:
            await client.send_photo(message.chat.id, image_url)
            await message.edit("Random anime image sent!")
        else:
            await message.edit("Failed to fetch a random anime image.")
    except Exception as e:
        await message.edit(f"Error: {e}")

def fetch_random_image(type, category):
    try:
        api_url = f"{BASE_URL}/{type}/{category}"

        response = requests.get(api_url)
        data = response.json()

        image_url = data["url"]

        return image_url
    except Exception as e:
        print("Failed to fetch a random image:", e)
        return None

add_command_help(
    "anime",
    [
        [f"randomanime", "Fetches a random anime image from a random SFW category and sends it in the chat."],
    ],
)
