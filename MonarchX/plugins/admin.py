import config
from pyrogram import filters, enums
from pyrogram.types import ChatPrivileges
from MonarchX import MonarchX, MODULE
from .help import add_command_help

@MonarchX.on_message(filters.command(["promote","fpromote"], prefixes=config.HANDLER) & filters.me)
async def promote_member(_, message):
     if message.reply_to_message:
          user_id = message.reply_to_message.from_user.id
     else:
        try:
           user_id = message.command[1]
        except:
            return await message.edit("Input username either id!")
     try:
         my_privileges = (await message.chat.get_member(user_id=message.from_user.id)).privileges 
         can_promote_members = [True if my_privileges and my_privileges.can_promote_members else False][0]
     except:
           return await message.edit("You aren't admin or you didn't have `can_promote_members` rights")
     command = message.command[0]
     if command == "fpromote" and can_promote_members:
              await message.chat.promote_member(user_id=user_id, privileges=my_privileges)
              return await message.edit("=> Fully Promoted!")
     elif command == "promote" and can_promote_members:
             privileges = ChatPrivileges(
                        can_delete_messages=True, can_restrict_members=True,
                        can_change_info=True, can_invite_users=True, can_pin_messages=True, can_manage_video_chats=True)
             await message.chat.promote_member(user_id=user_id, privileges=privileges)
             return await message.edit("=> Promoted!")

@MonarchX.on_message(filters.command(["demote"], prefixes=config.HANDLER) & filters.me)
async def demote_member(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id = message.command[1]
        except:
            return await message.edit("Reply to a message or provide a username or user ID!")

    try:
        my_privileges = (await message.chat.get_member(user_id=message.from_user.id)).privileges 
        can_promote_members = my_privileges.can_promote_members
    except:
        return await message.edit("You aren't an admin or you don't have `can_promote_members` rights")

    if can_promote_members:
        privileges = ChatPrivileges(
            can_delete_messages=False, can_restrict_members=False,
            can_change_info=False, can_invite_users=False,
            can_pin_messages=False, can_manage_video_chats=False
        )
        await message.chat.promote_member(user_id=user_id, privileges=privileges)
        return await message.edit("=> Demoted!")
    else:
        return await message.edit("You don't have permission to demote members.")
                     


@MonarchX.on_message(filters.command(["pin","unpin"], prefixes=config.HANDLER) & filters.me)
async def messages_pin(_, message):
      if not message.reply_to_message:
           return await message.edit("No Reply?")
      else:
         try:
            command = message.text[1:].casefold()
         except Exception as e:
              return await message.edit_text(f"Somthing Wrong Happens:\n{e}")
         link = message.reply_to_message.link
         if command == "pin":    
             try:
                 await message.reply_to_message.pin()
             except Exception as e:
                 return await message.edit_text(f"Somthing Wrong Happens:\n{e}")
             return await message.edit(f"Successfully [Pinned]({link})!")
         elif command == "unpin":
               try:
                   await message.reply_to_message.unpin()
               except Exception as e:
                   return await message.edit_text(f"Somthing Wrong Happens:\n{e}")
               return await message.edit(f"Successfully [UnPinned]({link})")


@MonarchX.on_message(filters.command("invite", prefixes=config.HANDLER) & filters.me)
async def invite_link(_, message):
     chat_id = message.chat.id
     try:
        link = (await MonarchX.get_chat(chat_id)).invite_link
     except Exception as e: 
         return await message.edit(f"Somthing Wrong Happens:\n{e}")
     return await message.edit(str(link))


@MonarchX.on_message(filters.command("del", prefixes=config.HANDLER) & filters.me)
async def delete_message(_, message):
     if message.reply_to_message:
         try:
            await message.reply_to_message.delete()
         except Exception as e:
              return await message.edit(f"Somthing wrong Happens:\n{e}")
         return await message.delete()
     else:
         return await message.edit("No Reply?")


@MonarchX.on_message(filters.command("ban", prefixes=config.HANDLER) & filters.me)
async def ban_member(_, message):
    if message.reply_to_message:
         user_id = message.reply_to_message.from_user.id  
    else:
      try:
         user_id = message.text.split()[1]
      except:
          return await message.edit("Provide USER_ID To Ban!")
    try:
       owo = await message.chat.ban_member(user_id)
    except Exception as e:
        return await message.edit(f"Somthing wrong Happens:\n{e}")
    name = (await MonarchX.get_users(user_id)).first_name
    return await message.edit(f"=> {name} Has Been Banned!")


@MonarchX.on_message(filters.command("unban", prefixes=config.HANDLER) & filters.me)
async def unban_member(_, message):
    if message.reply_to_message:
         user_id = message.reply_to_message.from_user.id  
    else:
      try:
         user_id = message.text.split()[1]
      except:
          return await message.edit("Provide USER_ID To UnBan!")
    try:
       owo = await message.chat.unban_member(user_id)
    except Exception as e:
        return await message.edit(f"Somthing wrong Happens:\n{e}")
    name = (await MonarchX.get_users(user_id)).first_name
    return await message.edit(f"=> {name} Has Been UnBanned!")


@MonarchX.on_message(filters.command("purge", prefixes=config.HANDLER) & filters.me)
async def purge(_, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        return await message.edit_text("No Reply?")
    else:
        reply_msg_id = message.reply_to_message.id
        message_id = message.id
        message_ids = []
        for ids in range(reply_msg_id, message_id):
            message_ids.append(ids)
        try:
           await MonarchX.delete_messages(chat_id=chat_id, message_ids=message_ids)
        except Exception as e:
              return await message.edit(f"Somthing wrong Happens:\n{e}")
        return await message.edit(f"=> Purged {len(message_ids)} Messages")

add_command_help(
    "admin",
    [
        [f"promote", "Promote a user to admin."],
        [f"deomote", "Denote a user to admin."],
        [f"fpromote", "Fully promote a user."],
        [f"pin", "Pin a message."],
        [f"unpin", "Unpin a message."],
        [f"invite", "Get the invite link for the chat."],
        [f"admins", "Get a list of chat admins."],
        [f"del", "Delete a message."],
        [f"ban", "Ban a user from the chat."],
        [f"unban", "Unban a user from the chat."],
        [f"purge", "Delete multiple messages at once."],
    ],
)
