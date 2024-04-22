import requests
from pyrogram import filters, Client
from pyrogram.types import Message, InputMediaPhoto
from MonarchX import MonarchX
from config import HANDLER,OWNER_ID
from pyrogram.errors import MediaCaptionTooLong
from .help import add_command_help


api_url_chat5 = "https://tofu-api.onrender.com/chat/bard"

def fetch_data(api_url: str, query: str) -> tuple:
    try:
        response = requests.get(f"{api_url}/{query}")
        response.raise_for_status()
        data = response.json()
        return data.get("content", "No response from the API."), data.get("images", False)
    except requests.exceptions.RequestException as e:
        return None, f"doRequest error: {e}"
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

@MonarchX.on_message(filters.command("bard", HANDLER) & filters.me)
async def chatgpt5(_, message: Message):
    chat_id = message.chat.id
    message_id = message.id
    
    if len(message.command) < 2:
        return await message.reply_text("Please provide a query.")

    query = " ".join(message.command[1:])
    txt = await message.reply_text("Wait patiently, requesting to API...")
    await txt.edit("💭")

    api_response, images = fetch_data(api_url_chat5, query)

    medias = []
    bard = str(api_response)
    try:
       photo_url = images[-1]
    except:
        pass
    
    
    if images:
        if len(images) > 1:
            for url in images:
                medias.append(InputMediaPhoto(media=url, caption=None))
                        
            medias[-1] = InputMediaPhoto(media=photo_url, caption=bard)
            
            try:
                await MonarchX.send_media_group(chat_id=chat_id, media=medias, reply_to_message_id=message_id)
                return await txt.delete()
            except Exception as e:
                return await txt.edit(str(e))
        elif len(images) < 2:
            image_url = images[0]
            try:
                await message.reply_photo(photo=image_url, caption=bard)
                return await txt.delete()
            except MediaCaptionTooLong:
                return await txt.edit(bard)
            except Exception as e:
                return await txt.edit(str(e))
        else:
            return await txt.edit('Somthing went wrong')
    else:
        try:
            return await txt.edit(bard)
        except Exception as e:
            return await txt.edit(str(e))
    
add_command_help(
    "bard",
    [
        ["bard [query]", "Generates text based on the provided query using the Bard API."],
    ]
)