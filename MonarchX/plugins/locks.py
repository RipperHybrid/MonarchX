from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import ChatNotModified
from pyrogram.types import ChatPermissions, Message

from config import HANDLER as cmd

from .help import add_command_help

incorrect_parameters = "Incorrect parameters. Type 'help locks' for assistance."

data = {
    "msg": "can_send_messages",
    "stickers": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "media": "can_send_media_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "url": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "info": "can_change_info",
    "invite": "can_invite_users",
    "pin": "can_pin_messages",
}


async def current_chat_permissions(client: Client, chat_id):
    perms = []
    perm = (await client.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")

    return perms


async def tg_lock(
    client: Client, message: Message, permissions: list, perm: str, lock: bool
):
    if lock:
        if perm not in permissions:
            return await message.edit_text("Already locked.")
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.edit_text("Already unlocked.")
        permissions.append(perm)

    permissions = {perm: True for perm in list(set(permissions))}

    try:
        await client.set_chat_permissions(
            message.chat.id, ChatPermissions(**permissions)
        )
    except ChatNotModified:
        return await message.edit_text(
            "To unlock this, you have to unlock 'messages' first."
        )

    await message.edit_text(("Locked." if lock else "Unlocked."))


@Client.on_message(filters.command(["lock", "unlock"], cmd) & filters.me)
async def locks_func(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.edit_text(incorrect_parameters)

    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()

    if parameter not in data and parameter != "all":
        return await message.edit_text(incorrect_parameters)

    permissions = await current_chat_permissions(client, chat_id)

    if parameter in data:
        await tg_lock(
            client,
            message,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        await client.set_chat_permissions(chat_id, ChatPermissions())
        await message.edit_text(f"Locked everything in {message.chat.title}")

    elif parameter == "all" and state == "unlock":
        await client.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False,
            ),
        )
        await message.edit(f"Unlocked everything in {message.chat.title}")


@Client.on_message(filters.command("locks", cmd) & filters.me)
async def locktypes(client: Client, message: Message):
    permissions = await current_chat_permissions(client, message.chat.id)

    if not permissions:
        return await message.edit("No permissions.")

    perms = ""
    for i in permissions:
        perms += f" • __**{i}**__\n"

    await message.edit_text(perms)


add_command_help(
    "locks",
    [
        ["lock <all or lock type>", "Lock permissions in a group."],
        [
            "unlock <all or unlock type>",
            "Unlock permissions in a group.\n\nSupported locks / unlocks: `msg` | `media` | `stickers` | `polls` | `info`  | `invite` | `webprev` | `pin` | `all`.",
        ],
    ],
)