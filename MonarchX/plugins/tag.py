from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import MessageIdInvalid
from pyrogram.types import Message

from config import HANDLER as cmd
from MonarchX.helpers.tools import get_arg

from .help import add_command_help

spam_chats = []


@Client.on_message(filters.command("tagall", cmd) & filters.me)
async def mentionall(client: Client, message: Message):
    chat_id = message.chat.id
    direp = message.reply_to_message
    args = get_arg(message)
    if not direp and not args:
        return await message.edit("**Give me a message or reply to a message!**")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}), "
        if usrnum == 5:
            try:
                if args:
                    txt = f"{args}\n{usrtxt}"
                    await client.send_message(chat_id, txt)
                elif direp:
                    await direp.reply(usrtxt)
            except MessageIdInvalid:
                pass
            await sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@Client.on_message(filters.command("cancel", cmd) & filters.me)
async def cancel_spam(client: Client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.edit("**Looks like there's no tagall here.**")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.edit("**Stopping Mentioning.**")


add_command_help(
    "tagall",
    [
        [
            "tagall [text/reply to chat]",
            "To Mention all members of the group",
        ],
        [
            "cancel",
            f"To Cancel the tagall command",
        ],
    ],
)