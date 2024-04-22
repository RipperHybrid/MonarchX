from telegraph import upload_file
from pyrogram import filters
from MonarchX import MonarchX, MODULE
from config import HANDLER,  OWNER_ID
from .help import add_command_help


@MonarchX.on_message(filters.command("tm", prefixes=HANDLER) & filters.me)
async def tm(_, message):
    await message.edit('processing...')
    reply_is = message.reply_to_message
    if not reply_is:
         return await message.edit_text("💔 Reply To The Media!")
    types = [True if reply_is.document else True if reply_is.photo else True if reply_is.animation else False][0]
    if types:
        path = await message.reply_to_message.download()
        grap = upload_file(path)
        for code in grap:
              url = "https://graph.org"+code
        return await message.edit(str(url))
        
add_command_help(
    "tm",
    [
        ["tm", "Uploads the replied media to Telegraph and returns the link."],
    ]
)