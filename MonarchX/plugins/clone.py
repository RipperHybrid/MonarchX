from MonarchX import MonarchX, MODULE
from pyrogram import filters
from MonarchX.MonarchX_db.clone_db import store_profile, get_profile
from .help import add_command_help
import config

@MonarchX.on_message(filters.command("cpfp",config.HANDLER) & filters.me)
async def clone(_, message):
    if not message.reply_to_message:
         try:
            clone_id = message.text.split(None,1)[1]
         except:
              return await message.edit("=> reply to the user either give a user id")
    else:
         clone_id = message.reply_to_message.from_user.id

    user_id = message.from_user.id
    
    if (await get_profile(user_id)) == False:
          return await message.edit_text("You didn't Saved Any Profile. Send ```.savepfp``` and try again.") 
           
          
    await message.edit('Collecting Information from Client')

    user = await MonarchX.get_chat(clone_id)
    bio = user.bio if user.bio else None
    first_name = user.first_name
    photo_id = user.photo.big_file_id if user.photo else None

    try:
       profile = await MonarchX.download_media(photo_id)
       await MonarchX.set_profile_photo(photo=profile)
    except:
        pass
   
    await MonarchX.update_profile(first_name=first_name, bio=bio)
    return await message.edit("✅ Successfully Implemented!")
    
    
    
@MonarchX.on_message(filters.command("savepfp", config.HANDLER) & filters.me)
async def save_pfp(_, message):
      user_id = message.from_user.id
      await message.edit('Saving your information into DB')      
      user = await MonarchX.get_chat(user_id)
      bio = user.bio if user.bio else None
      first_name = user.first_name 
      async for file in MonarchX.get_chat_photos(user_id, limit=1):
             photo_id = file.file_id if user.photo else None
      await store_profile(user_id=user_id, profile=photo_id, first_name=first_name, bio=bio)
      return await message.edit("Successfully Saved!")
          
@MonarchX.on_message(filters.command("rnpfp", config.HANDLER) & filters.me)
async def return_profile(_, message):
     user_id = message.from_user.id
     if (await get_profile(user_id)) == False:
         return await message.edit("Use ```.savepfp``` save your information and try again.")      
     user = await get_profile(user_id)
     bio = user.get("bio")
     first_name = user.get("first_name")
     photo_id = user.get("profile")
     try:
        profile = await MonarchX.download_media(photo_id)
        await MonarchX.set_profile_photo(photo=profile)
     except:
         pass

     await MonarchX.update_profile(first_name=first_name, bio=bio)
     return await message.edit("Successfully Reseted Info!")


add_command_help(
    "profile",
    [
        ["cpfp `or` clone", "Clone the profile of a user."],
        ["savepfp", "Save your profile information."],
        ["rnpfp", "Restore your saved profile information."],
    ],
)