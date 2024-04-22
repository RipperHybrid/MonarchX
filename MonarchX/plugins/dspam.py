import asyncio
from pyrogram.types import Message
from pyrogram import filters
from MonarchX import MonarchX, MODULE
import config
from .help import add_command_help


@MonarchX.on_message(filters.command(["ds"], prefixes=config.HANDLER) & filters.me)
async def delay_handler(_, m: Message):
    try:
        reply = m.reply_to_message
        cmd = m.command

        if len(m.command) < 3:
            await MonarchX.send_message(m.chat.id, f"Use like this: `{config.HANDLER}dspam [count spam] [delay time in seconds] [text messages]`")

        elif len(m.command) > 2 and not reply:
            await m.delete()
            msg = m.text.split(None, 3)
            times = int(msg[1]) if msg[1].isdigit() else None
            sec = int(msg[2]) if msg[2].isdigit() else None
            text = msg[3]
            for x in range(times):
                await MonarchX.send_message(
                    m.chat.id,
                    text
                )
                await asyncio.sleep(sec)
        else:
            await MonarchX.send_message(m.chat.id, "Something wrong in spam command !")
    except Exception as e:
        print(e)  # Print the error to the console for debugging purposes


# For spam command Made by @daanav_asura

@MonarchX.on_message(filters.command(["spam"], prefixes=config.HANDLER) & filters.me)
async def spam_handler(_, m: Message):
    try:
        reply = m.reply_to_message
        reply_to_id = reply.message_id if reply else None
        cmd = m.command

        if not reply and len(cmd) < 2:
            await MonarchX.send_message(m.chat.id, f"Use like this: {config.HANDLER}spam [count spam] [text messages]")
            return

        if not reply and len(cmd) > 1:
            await m.delete()
            times = int(cmd[1]) if cmd[1].isdigit() else None
            text = " ".join(cmd[2:]).strip()
            if not text:
                await MonarchX.send_message(m.chat.id, "The spam text cannot be empty.")
                return

            for x in range(times):
                await MonarchX.send_message(
                    m.chat.id,
                    text
                )
                await asyncio.sleep(0.10)

        elif reply:
            await m.delete()
            times = int(cmd[1]) if cmd[1].isdigit() else None
            for x in range(times):
                await MonarchX.copy_message(
                    m.chat.id,
                    m.chat.id,
                    reply.message_id
                )
    except Exception as e:
        print(e)  # Print the error to the console for debugging purposes


@MonarchX.on_message(filters.command(["say"], prefixes=config.HANDLER) & filters.me)
async def say(_, m: Message):
    chat_id = m.chat.id
    cmd = m.command
    text = " ".join(cmd[1:]).strip()
    if len(cmd) < 2:
        await MonarchX.reply_text(f"Provide text.eg {config.HANDLER}.say [text messages]")
        return
    try:
        await m.delete()
    except:
        return
    await MonarchX.send_message(chat_id,text)

@MonarchX.on_message(filters.command(["smsg"], prefixes=config.HANDLER) & filters.me)
async def send_msg(_, m: Message):
    id = int(m.command[1])
    cmd = m.command
    text = " ".join(cmd[2:]).strip()

    if len(cmd) < 2:
        await m.reply_text(f"Use like this: {config.HANDLER}smsg [user/chatid] [text messages]")
        return
    msg =  await m.reply_text("Trying to send msg...")
    
    try:
        await MonarchX.send_message(id,text)
        await msg.edit("Sent Successfully")
    except Exception as err:
        await msg.edit(f"Error Occured!\n{err}")
    try:
        await m.delete()
    except:
        return
    

add_command_help(
    "spam",
    [
        ["spam", "Send multiple identical messages in a chat."],
        ["say", "Send a message in the chat."],
        ["smsg", "Send a message to a user or chat by ID."],
        ["ds", "Send multiple identical messages with a delay between each message."],
    ],
)