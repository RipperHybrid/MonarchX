from prettytable import PrettyTable
from pyrogram import Client, filters
from pyrogram.types import Message

from config import HANDLER
from MonarchX import CMD_HELP
from MonarchX.helpers.basic import edit_or_reply
from MonarchX.helpers.utility import split_list


@Client.on_message(filters.command("help", HANDLER) & filters.me)
async def module_help(client: Client, message: Message):
    cmd = message.command
    help_arg = ""
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        help_arg = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        ac = PrettyTable()
        ac.header = False
        ac.title = "MonarchX Modules"
        ac.align = "l"
        for x in split_list(sorted(CMD_HELP.keys()), 2):
            ac.add_row([x[0], x[1] if len(x) >= 2 else None])
        await edit_or_reply(
            message, f"```{str(ac)}```\n• @Ripper_Hybrid •"
        )
        await message.reply(
            f"**Example type** `{HANDLER}help afk` **to view module information.**"
        )

    if help_arg:
        if help_arg in CMD_HELP:
            commands: dict = CMD_HELP[help_arg]
            this_command = f"──「 **Help For {str(help_arg).upper()}** 」──\n\n"
            for x in commands:
                this_command += f"  •  **Command:** `{HANDLER}{str(x)}`\n  •  **Function:** `{str(commands[x])}`\n\n"
            this_command += "© @Ripper_Hybrid"
            await edit_or_reply(
                message, this_command
            )
        else:
            await edit_or_reply(
                message,
                f"`{help_arg}` **is not a valid module name.**",
            )


def add_command_help(module_name, commands):
    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    for x in commands:
        for y in x:
            if y is not x:
                command_dict[x[0]] = x[1]

    CMD_HELP[module_name] = command_dict