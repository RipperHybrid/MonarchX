import importlib
import pyrogram
import strings
import config

from MonarchX import bot , MonarchX
from MonarchX.helpers.help_func import get_datetime 

async def run_clients():
      await bot.start()
      await MonarchX.start()
      await pyrogram.idle()
      zone = await get_datetime()
      await bot.send_message(
           chat_id=config.GROUP_ID,
           text=strings.RESTART_TEXT1.format(date=zone["date"], time=zone["time"]))
      await MonarchX.send_message(
           chat_id=config.GROUP_ID,
           text=strings.RESTART_TEXT2.format(date=zone["date"], time=zone["time"]))


if __name__ == "__main__":
    config.HANDLER = ["~", ".", "!", "?", "@", "$"]
    default_handler = config.HANDLER[0] if config.HANDLER else "."
    MonarchX.loop.run_until_complete(run_clients())
