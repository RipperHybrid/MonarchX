from MonarchX import MonarchX 
from MonarchX import bot, INFO as GET_INFO
from MonarchX.plugins.alive import alive
from pyrogram import filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultPhoto,
)

@bot.on_inline_query(filters.regex("alive"))
async def alive_inline(_, inline_query):
    user_id = inline_query.from_user.id
    if user_id == GET_INFO().id:
        ALIVE_TEXT, photo_url = await alive()
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🗿 Owner", url="https://t.me/Ripper_Hybrid"),
                ],
            ]
        )

        await bot.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                InlineQueryResultPhoto(
                    title="🤖 Bot Status",
                    caption=ALIVE_TEXT,
                    photo_url=photo_url,
                    thumb_url="https://graph.org/file/b136511bda43b1d8db7d2.jpg",
                    reply_markup=buttons,
                )
            ]
        )
    else:
        await bot.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[]
        )
