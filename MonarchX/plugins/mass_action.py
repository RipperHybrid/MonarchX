from pyrogram import filters, enums
from pyrogram.types import *
from MonarchX import MonarchX as bot
from config import HANDLER, OWNER_ID
from .help import add_command_help
import asyncio

async def is_owner(chat_id: int, user_id: int):
    async for x in bot.get_chat_members(chat_id):
        if x.status == enums.ChatMemberStatus.OWNER:
             if x.user.id == user_id:
                 return True
             else: return False



@bot.on_message(filters.me & filters.command(["unbanall","massunban"], prefixes=HANDLER))
async def unbanall(_, message):
     user_id = message.from_user.id
     chat_id = message.chat.id
     if user_id not in OWNER_ID and not await is_owner(chat_id, user_id):
          return await message.edit("`You Can't Access This!`")
     elif message.chat.type == enums.ChatType.PRIVATE:
          return await message.edit("`This Command Only work in Groups!`")
     else:
       try:
          BANNED = []
          unban = 0
          async for m in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
                 BANNED.append(m.user.id)
                 await bot.unban_chat_member(chat_id,m.user.id)
                 unban +=1
          await message.edit("**Found Banned Members**: `{}`\n**Unbanned Successfully**: `{}`".format(len(BANNED), unban))
       except Exception as e:
           print(e)
          

@bot.on_message(filters.me & filters.command(["sbanall","banall","massban"], prefixes=HANDLER))
async def banall(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id not in OWNER_ID and (await is_owner(chat_id,user_id)) == False:
         return await message.edit("`You Can't Access This!`")
    elif message.chat.type == enums.ChatType.PRIVATE:
         return await message.edit("`This Command Only work in Groups!`")
    else:  
       try: 
          Members = []
          Admins = []
          async for x in bot.get_chat_members(chat_id):
              if not x.privileges:
                    Members.append(x.user.id)
              else:
                    Admins.append(x.user.id)
          for user_id in Members:
               if message.text.split()[0].lower().startswith("s"):
                        m = await bot.ban_chat_member(chat_id, user_id)
                        await m.delete()
               else:
                   await bot.ban_chat_member(chat_id, user_id)
          await message.edit_text("**Successfully Banned**: `{}`\n**Remaining Admins**: `{}`".format(len(Members),len(Admins),))
       except Exception as e:
        print(e)
     

@bot.on_message(filters.me & filters.command(["skickall","kickall","masskick"], prefixes=HANDLER))
async def kickall(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id not in OWNER_ID and (await is_owner(chat_id,user_id)) == False:
          return await message.edit("`You Can't Access This!`")
    elif message.chat.type == enums.ChatType.PRIVATE:
          return await message.edit("`This Command Only work in Groups!`")
    else:  
       try: 
          Members = []
          Admins = []
          async for x in bot.get_chat_members(chat_id):
              if not x.privileges:
                    Members.append(x.user.id)
              else:
                    Admins.append(x.user.id)
          for user_id in Members:
               if message.text.split()[0].lower().startswith("s"):
                        m = await bot.ban_chat_member(chat_id, user_id)
                        await bot.unban_chat_member(chat_id, user_id)
                        await m.delete()
               else:
                   await bot.ban_chat_member(chat_id, user_id)
                   await bot.unban_chat_member(chat_id, user_id)
          await message.edit_text("**Successfully Kicked**: `{}`\n**Remaining Admins**: `{}`".format(len(Members),len(Admins),))
       except Exception as e:
        print(e)


@bot.on_message(filters.me & filters.command(["muteall"], prefixes=HANDLER))
async def mute_all(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id not in OWNER_ID and not await is_owner(chat_id, user_id):
        return await message.edit("`You Can't Access This!`")
    elif message.chat.type == enums.ChatType.PRIVATE:
        return await message.edit("`This Command Only works in Groups or Channels!`")
    else:
        try:
            total_members = 0
            muted_members = 0
            async for member in bot.get_chat_members(chat_id):
                total_members += 1
                if member.user.id != bot.me.id and member.status != enums.ChatMemberStatus.ADMINISTRATOR:
                    await bot.restrict_chat_member(
                        chat_id,
                        member.user.id,
                        ChatPermissions(
                            can_send_messages=False,
                            can_send_media_messages=False,
                            can_send_polls=False,
                            can_send_other_messages=False,
                            can_add_web_page_previews=False,
                            can_change_info=False,
                            can_invite_users=False,
                            can_pin_messages=False,
                        ),
                    )
                    muted_members += 1
                    await message.reply(f"Muted user: {member.user.id}")
            await message.edit(f"Total users: {total_members}\nMuted users: {muted_members}")
        except Exception as e:
            print(e)

@bot.on_message(filters.me & filters.command(["unmuteall"], prefixes=HANDLER))
async def unmute_all(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id not in OWNER_ID and not await is_owner(chat_id, user_id):
        return await message.edit("`You Can't Access This!`")
    elif message.chat.type == enums.ChatType.PRIVATE:
        return await message.edit("`This Command Only works in Groups or Channels!`")
    else:
        try:
            found_muted = 0
            unmuted_members = 0
            async for member in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED):
                if member.user.id != bot.me.id and member.status != enums.ChatMemberStatus.ADMINISTRATOR:
                    found_muted += 1
                    await bot.restrict_chat_member(
                        chat_id,
                        member.user.id,
                        ChatPermissions(
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_polls=True,
                            can_send_other_messages=True,
                            can_add_web_page_previews=True,
                            can_change_info=True,
                            can_invite_users=True,
                            can_pin_messages=True,
                        ),
                    )
                    unmuted_members += 1
                    await message.reply(f"Unmuted user: {member.user.id}")
            await message.edit(f"Found Muted Users: {found_muted}\nUnmuted Users: {unmuted_members}")
        except Exception as e:
            print(e)
            
            
@bot.on_message(filters.me & filters.command(["emute"], prefixes=HANDLER))
async def emute(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.edit("`This Command Only works in Groups or Channels!`")
    else:
        try:
            total_members = 0
            muted_members = 0
            async for member in bot.get_chat_members(chat_id):
                total_members += 1
                if member.user.id != bot.me.id and member.user.id != user_id:
                    await bot.restrict_chat_member(
                        chat_id,
                        member.user.id,
                        ChatPermissions(
                            can_send_messages=False,
                            can_send_media_messages=False,
                            can_send_polls=False,
                            can_send_other_messages=False,
                            can_add_web_page_previews=False,
                            can_change_info=False,
                            can_invite_users=False,
                            can_pin_messages=False,
                        ),
                    )
                    muted_members += 1
                    await message.reply(f"Muted user: {member.user.id}")
            await message.edit(f"Total users: {total_members}\nMuted users: {muted_members}")
        except Exception as e:
            print(e)


@bot.on_message(filters.me & filters.command(["unbanchannel"], prefixes=HANDLER))
async def unbanchannel(_, message):
    user_id = message.from_user.id
    chat_id = -1002052259061
    if user_id not in OWNER_ID and (await is_owner(chat_id, user_id)) == False:
        return await message.edit("`You Can't Access This!`")
    elif message.chat.type not in [enums.ChatType.CHANNEL, enums.ChatType.SUPERGROUP]:
        return await message.edit("`This Command Only works in Channels or Supergroups!`")
    
    await message.edit("Unbanning to all wait for 1 hour")

    try:
        BANNED = []
        unban = 0
        async for m in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
            BANNED.append(m.user.id)
            await bot.unban_chat_member(chat_id, m.user.id)
            unban += 1
        await message.edit("**Found Banned Channel Members**: `{}`\n**Unbanned Successfully**: `{}`".format(len(BANNED), unban))
    except Exception as e:
        print(e)


add_command_help(
    "action",
    [
        ["banall", "Ban all members in the chat."],
        ["kickall", "Kick all members in the chat."],
        ["muteall", "Mute all members in the chat."],
        ["unbanall", "Unban all currently banned users in the chat."],
        ["unmuteall", "Unmute all currently muted users in the chat."],
    ]
)
