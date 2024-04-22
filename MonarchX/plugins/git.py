from pyrogram import filters 
from MonarchX import MonarchX, MODULE
from requests import get
from .help import add_command_help

import os
import config

@MonarchX.on_message(filters.me & filters.command("git",prefixes=config.HANDLER))
async def git(_, message):
    if len(message.command) < 2:
        return await message.reply_text("where you input the username?\n")
    user = message.text.split(None, 1)[1]
    res = get(f'https://api.github.com/users/{user}').json()
    data = f"""**Name**: {res['name']}
**UserName**: {res['login']}
**Link**: [{res['login']}]({res['html_url']})
**Bio**: {res['bio']}
**Company**: {res['company']}
**Blog**: {res['blog']}
**Location**: {res['location']}
**Public Repos**: {res['public_repos']}
**Followers**: {res['followers']}
**Following**: {res['following']}
**Acc Created**: {res['created_at']}
"""
    with open(f"{user}.jpg", "wb") as f:
        kek = get(res['avatar_url']).content
        f.write(kek)

    await message.reply_photo(f"{user}.jpg", caption=data)
    os.remove(f"{user}.jpg")
    await message.delete()
    return 

add_command_help(
    "git",
    [
        ["git [username]", "Fetches GitHub user information and displays it with a photo."],
    ],
)