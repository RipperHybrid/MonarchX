import requests
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from .help import add_command_help

from config import HANDLER as cmd

BASE_URL = "https://animechan.xyz/api/"

@Client.on_message(filters.command(["rq", "qtitle", "qcharacter", "qpagination"], cmd) & filters.me)
async def anime_quote(client: Client, message: Message):
    command = message.command[0].lower()

    if command == "rq":
        await random_quote(client, message)
    elif command == "qtitle":
        await quote_by_title(client, message)
    elif command == "qcharacter":
        await quote_by_character(client, message)
    elif command == "qpagination":
        await quote_with_pagination(client, message)

async def random_quote(client: Client, message: Message):
    await message.edit("Fetching a random anime quote...")

    try:
        quote = fetch_random_quote()
        if quote:
            quote_text = f"Anime: {quote['anime']}\nCharacter: {quote['character']}\nQuote: {quote['quote']}"
            await message.edit(quote_text)
        else:
            await message.edit("Failed to fetch a random anime quote.")
    except Exception as e:
        await message.edit(f"Error: {e}")

async def quote_by_title(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit("Please provide an anime title.")
        return

    anime_title = " ".join(message.command[1:])
    await message.edit(f"Fetching anime quotes for title: {anime_title}...")

    try:
        quotes = fetch_quote_by_title(anime_title)
        if quotes:
            random_quote = random.choice(quotes)
            quote_text = f"Anime: {random_quote['anime']}\nCharacter: {random_quote['character']}\nQuote: {random_quote['quote']}"
            await message.edit(quote_text)
        else:
            await message.edit("No quotes found for the provided anime title.")
    except Exception as e:
        await message.edit(f"Error: {e}")

async def quote_by_character(client: Client, message: Message):
    if len(message.command) < 2:
        await message.edit("Please provide an anime character name.")
        return

    character_name = " ".join(message.command[1:])
    await message.edit(f"Fetching anime quotes for character: {character_name}...")

    try:
        quotes = fetch_quote_by_character(character_name)
        if quotes:
            random_quote = random.choice(quotes)
            quote_text = f"Anime: {random_quote['anime']}\nCharacter: {random_quote['character']}\nQuote: {random_quote['quote']}"
            await message.edit(quote_text)
        else:
            await message.edit("No quotes found for the provided character name.")
    except Exception as e:
        await message.edit(f"Error: {e}")

async def quote_with_pagination(client: Client, message: Message):
    if len(message.command) < 3:
        await message.edit("Please provide an anime title and page number.")
        return

    anime_title = message.command[1]
    page_number = int(message.command[2])
    await message.edit(f"Fetching anime quotes for title: {anime_title}, page: {page_number}...")

    try:
        quotes = fetch_quotes_with_pagination(anime_title, page_number)
        if quotes:
            random_quote = random.choice(quotes)
            quote_text = f"Anime: {random_quote['anime']}\nCharacter: {random_quote['character']}\nQuote: {random_quote['quote']}"
            await message.edit(quote_text)
        else:
            await message.edit("No quotes found for the provided anime title and page number.")
    except Exception as e:
        await message.edit(f"Error: {e}")

def fetch_random_quote():
    try:
        response = requests.get(BASE_URL + "random")
        quote = response.json()
        return quote
    except Exception as e:
        print("Failed to fetch a random quote:", e)
        return None

def fetch_quote_by_title(anime_title):
    try:
        response = requests.get(f"{BASE_URL}/quotes/anime?title={anime_title}")
        quotes = response.json()
        return quotes
    except Exception as e:
        print("Failed to fetch quotes by anime title:", e)
        return None

def fetch_quote_by_character(character_name):
    try:
        response = requests.get(f"{BASE_URL}/quotes/character?name={character_name}")
        quotes = response.json()
        return quotes
    except Exception as e:
        print("Failed to fetch quotes by anime character:", e)
        return None

def fetch_quotes_with_pagination(anime_title, page):
    try:
        response = requests.get(f"{BASE_URL}/quotes/anime?title={anime_title}&page={page}")
        quotes = response.json()
        return quotes
    except Exception as e:
        print("Failed to fetch quotes with pagination:", e)
        return None

add_command_help(
    "quote",
    [
        [f"rq", "Fetches a random anime quote and sends it in the chat."],
        [f"qtitle [anime_title]", "Fetches a random anime quote by title and sends it in the chat."],
        [f"qcharacter [character_name]", "Fetches a random anime quote by character and sends it in the chat."],
        [f"qpagination [anime_title] [page_number]", "Fetches a random anime quote with pagination and sends it in the chat."],
    ],
)