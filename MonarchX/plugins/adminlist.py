import html
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums

from config import HANDLER as cmd
from MonarchX.helpers.basic import edit_or_reply
from MonarchX.helpers.parser import mention_html, mention_markdown
from .help import add_command_help


@Client.on_message(filters.me & filters.command(["admins", "adminlist"], cmd))
async def adminlist(client: Client, message: Message):
    await message.edit("Analyzing admins...")

    replyid = None
    toolong = False
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.id
    creator = []
    admin = []
    badmin = []
    async for a in client.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.custom_title:
            nama += f" | {a.custom_title}" 
        if a.status == enums.ChatMemberStatus.ADMINISTRATOR:
            if a.user.is_bot:
                badmin.append(mention_markdown(a.user.id, nama))
            else:
                admin.append(mention_markdown(a.user.id, nama))
        elif a.status == enums.ChatMemberStatus.OWNER:
            creator.append(mention_markdown(a.user.id, nama))
    admin.sort()
    badmin.sort()
    totaladmins = len(creator) + len(admin) + len(badmin)
    teks = "**Admins in {}**\n".format(grup.title)
    teks += "╒═══「 Creator 」\n"
    for x in creator:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "╞══「 {} Human Administrator 」\n".format(len(admin))
    for x in admin:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "╞══「 {} Bot Administrator 」\n".format(len(badmin))
    for x in badmin:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "╘══「 Total {} Admins 」".format(totaladmins)
    if toolong:
        await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.edit(teks)

@Client.on_message(filters.command(["kickdel", "zombies"], cmd) & filters.me)
async def kickdel_cmd(client, message):
    Man = await message.edit("<b>Kicking deleted accounts...</b>")
    
    values = []
    chat_id = message.chat.id
    
    try:
        chat = await client.get_chat(chat_id)
        members = await chat.get_members()
        
        for member in members:
            if member.user.is_deleted:
                await client.kick_chat_member(chat_id, member.user.id, int(time()) + 31)
                values.append(member)
    except Exception as e:
        await Man.edit(f"<b>Error: {e}</b>")
        return
    
    await Man.edit(f"<b>Successfully kicked {len(values)} deleted account(s)</b>")
    
@Client.on_message(
    filters.me & filters.command(["reportadmin", "reportadmins", "report"], cmd)
)
async def report_admin(client: Client, message: Message):
    await message.delete()
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = None
    grup = await client.get_chat(message.chat.id)
    admin = []
    async for a in client.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        if (
            a.status == enums.ChatMemberStatus.ADMINISTRATOR
            or a.status == enums.ChatMemberStatus.OWNER
        ):
            if not a.user.is_bot:
                admin.append(mention_html(a.user.id, "\u200b"))
    if message.reply_to_message:
        if text:
            teks = "{}".format(text)
        else:
            teks = "{} reported to admins.".format(
                mention_html(
                    message.reply_to_message.from_user.id,
                    message.reply_to_message.from_user.first_name,
                )
            )
    else:
        if text:
            teks = "{}".format(html.escape(text))
        else:
            teks = "Calling admins in {}.".format(grup.title)
    teks += "".join(admin)
    if message.reply_to_message:
        await client.send_message(
            message.chat.id,
            teks,
            reply_to_message_id=message.reply_to_message.id,
            parse_mode=enums.ParseMode.HTML,
        )
    else:
        await client.send_message(
            message.chat.id, teks, parse_mode=enums.ParseMode.HTML
        )


@Client.on_message(filters.me & filters.command(["botlist", "bots"], cmd))
async def get_list_bots(client: Client, message: Message):
    replyid = None
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.id
    getbots = client.get_chat_members(chat)
    bots = []
    async for a in getbots:
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.user.is_bot:
            bots.append(mention_markdown(a.user.id, nama))
    teks = "**All bots in group {}**\n".format(grup.title)
    teks += "╒═══「 Bots 」\n"
    for x in bots:
        teks += "│ • {}\n".format(x)
    teks += "╘══「 Total {} Bots 」".format(len(bots))
    if replyid:
        await client.send_message(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.edit(teks)

@Client.on_message(filters.me & filters.command(["gc", "gci"], cmd))
async def group_info(client: Client, message: Message):
    try:
        await message.edit("Fetching group info...")

        chat_info = await client.get_chat(message.chat.id)

        if isinstance(chat_info, str):
            raise ValueError("Received unexpected string instead of chat info.")

        title = chat_info.title
        chat_type = chat_info.type
        members_count = chat_info.members_count
        description = chat_info.description if hasattr(chat_info, 'description') else None
        chat_id = chat_info.id
        username = chat_info.username

        info_text = f"ℹ️ Group Info\n\n"
        info_text += f"Title: {title}\n"
        info_text += f"Type: {chat_type}\n"
        info_text += f"Members Count: {members_count}\n"

        if description:
            info_text += f"Description: {description}\n"

        info_text += f"ID: {chat_id}\n"
        if username:
            info_text += f"Username: @{username}\n"

        info_text = "```\n" + info_text + "```"

        await message.edit(info_text)

    except Exception as e:
        await message.edit(f"Failed to fetch group info: {str(e)}")
        
add_command_help(
    "tag",
    [
        [f"admins", "Get chats Admins list."],
        [f"kickdel", "To Kick deleted Accounts."],
        [
            f"everyone `or` tagall",
            "to mention Everyone ",
        ],
        [
            f"botlist",
            "To get Chats Bots list",
        ],
        [
            f"gc",
            "To fetch group/supergroup information",
        ],
    ],
)
