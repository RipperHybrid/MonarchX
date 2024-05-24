import re
from pyrogram import Client, filters
from pyrogram.types import Message
from config import HANDLER
from .help import add_command_help

@Client.on_message(filters.command("calc", HANDLER) & filters.me)
async def calc(client: Client, message: Message):
    expression = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else ""
    if not expression:
        return await message.reply_text("Please provide a mathematical expression to calculate.")
    
    allowed_chars = re.compile(r'^[\d+\-*/(). ]+$')
    if not allowed_chars.match(expression):
        return await message.reply_text("Invalid characters in expression. Only digits and + - * / ( ) are allowed.")
    
    try:
        result = eval(expression)
        await message.reply_text(f"The result is: {result}")
    except Exception as e:
        await message.reply_text(f"Error in calculation: {str(e)}")

add_command_help(
    "calc",
    [
        ["calc", "Calculate a mathematical expression. Usage: calc 2+3-1*4/2"],
    ]
)
