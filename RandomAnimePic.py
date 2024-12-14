#  _  __  ___   ____  _   _ 
# | |/ / | __| |_  / | | | |
# | ' <  | _|   / /  | |_| |
# |_|\_\ |___| /___|  \___/
#
#  __  __    ___    ___    ___ 
# |  \/  |  / _ \  |   \  / __|
# | |\/| | | (_) | | |) | \__ \
# |_|  |_|  \___/  |___/  |___/
#

# meta developer: @dummykezu

from .. import loader, utils
from telethon.tl.types import InputMessagesFilterPhotos
import random

@loader.tds
class RandomAnimePicMod(loader.Module):
    strings = {
        "name": "RandomAnimePic",
        "your_pic": "⚡ <b>Your pic</b>",
    }
    strings_ru = {
        "your_pic": "⚡ <b>Ваше изображение</b>",
    }

    @loader.command(ru_doc="Получить рандомное изображение.")
    async def rapiccmd(self, message):
        """Fetch random pic."""
        await message.delete()
        channel = "@auygram_vf"
        total = (await message.client.get_messages(channel, limit=0, filter=InputMessagesFilterPhotos)).total
        
        if total > 0:
            random_offset = random.randint(0, total - 1)
            random_pic = await message.client.get_messages(channel, filter=InputMessagesFilterPhotos, limit=1, add_offset=random_offset)
            if random_pic:
                await message.client.send_file(
                    message.chat_id,
                    random_pic[0].media,
                    caption=self.strings("your_pic"),
                    reply_to=message.reply_to_msg_id
                )