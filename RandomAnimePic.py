# _  __  ___   ____  _   _ 
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

import requests
import asyncio
from .. import loader, utils

@loader.tds
class RandomAnimePicMod(loader.Module):
  strings = {
    "name": "RandomAnimePic",
    "img": "<emoji document_id=4916036072560919511>✅</emoji> <b>Your anime pic</b>",
    "loading": "<emoji document_id=4911241630633165627>✨</emoji> <b>Loading image...</b>",
    "error": "<emoji document_id=5116151848855667552>🚫</emoji> <b>An unexpected error occurred...</b>",
  }
  
  strings_ru = {
    "img": "<emoji document_id=4916036072560919511>✅</emoji> <b>Ваша аниме-картинка</b>",
    "loading": "<emoji document_id=4911241630633165627>✨</emoji> <b>Загрузка изображения...</b>",
    "error": "<emoji document_id=5116151848855667552>🚫</emoji> <b>Произошла непредвиденная ошибка...</b>",
  }
  
  @loader.command(
    ru_doc="- получить рандомную аниме-картинку 👀"
  )
  async def rapiccmd(self, message):
    """- fetch random anime-pic 👀"""
    
    try:
      msg = await utils.answer(message, self.strings("loading"))
      
      res = requests.get("https://api.nekosia.cat/api/v1/images/cute?count=1")
      res.raise_for_status()
      data = res.json()
      
      await asyncio.sleep(2)
      
      await msg.delete()
      
      await self._client.send_file(message.peer_id, data['image']['original']['url'], caption=self.strings("img"), reply=message.reply_to_msg_id)
    
    except Exception:
      msg = await utils.answer(message, self.strings("error"))
      
      await asyncio.sleep(5)
      
      await msg.delete()