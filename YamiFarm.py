# meta developer: @shiningwhore

import asyncio
import random
from .. import loader, utils

class YamiFarmMod(loader.Module):
    """YamiChat бот автофарм"""
    strings = {"name": "YamiFarm"}
    
    def init(self):
        super().init()

    async def yfarkick(self):
        while self.db.get("YamiFarm", "farming", False):
            try:
                await self._client.send_message("@YamiChat_bot", "фарм")
                await asyncio.sleep(random.randint(3600, 3800))
            except Exception as e:
                self.db.set("YamiFarm", "farming", False)
                return
    
    async def yfarmcmd(self, message):
        """Включить/выключить автофарм .yfarm on/off"""
        args = utils.get_args_raw(message)
        if args == "on":
            if not self.db.get("YamiFarm", "farming", False):
                self.db.set("YamiFarm", "farming", True)
                asyncio.create_task(self.yfarkick())
                await utils.answer(message, "Автофарм включен")
            else:
                await utils.answer(message, "<b>Автофарм уже запущен!</b>")
        elif args == "off":
            if self.db.get("YamiFarm", "farming", False):
                self.db.set("YamiFarm", "farming", False)
                await utils.answer(message, "<b>Автофарм выключен</b>")
            else:
                await utils.answer(message, "<b>Автофарм не был запущен!</b>")
        else:
            await utils.answer(message, "<b>Используйте</b> <code>.yfarm on/off</code>")
    
    async def ybalcmd(self, message):
        """Проверить баланс .ybal"""
        chat = "@YamiChat_bot"
        msg = await self._client.send_message(chat, "кеш")
        await asyncio.sleep(2)
        response = await self._client.get_messages(chat, limit=1)
        await msg.delete()
        await response[0].delete()
        await utils.answer(message, f"{response[0].message}")
