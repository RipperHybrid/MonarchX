import asyncio
import config
from MonarchX import bot, INFO
from MonarchX.helpers.help_func import emoji_convert
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

SPAM = []

@bot.on_message(filters.command("start") & filters.private)
async def start_command(_, message):
    user_id = message.from_user.id
    
    if user_id in SPAM:
        return await message.reply("`Please don't spam this command.`")

    SPAM.append(user_id)

    info = await INFO.MonarchX()
    botlive = await emoji_convert(bot.is_connected)
    applive = await emoji_convert(bot.is_connected)
    name = info.first_name
    id = info.id
    
    mention = f"[{name}](tg://user?id={id})"
    BUTTON = InlineKeyboardMarkup([
        [InlineKeyboardButton("SOURCE 👾", url=config.SOURCE)],
    ])

    start_message = (
        f"Hello {mention}!\n\n"
        f"I am {mention} Telegram bot.\n"
        f"Bot Status: {botlive}\n"
        f"App Status: {applive}"
    )

    await message.reply_text(
        text=start_message,
        quote=True,
        reply_markup=BUTTON,
        parse_mode=enums.ParseMode.MARKDOWN
    )

    await asyncio.sleep(20)
    SPAM.remove(user_id)
