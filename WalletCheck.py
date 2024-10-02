# meta developer: @htmIpage
# author: Не знаю, чья идея. Если есть претензии ко мне — профиль из meta developer к вашим услугам.

from .. import loader, utils
import telethon

class WalletCheckMod(loader.Module):
    """Модуль для взаимодействия с @send"""
    strings = {'name': 'WalletCheck'}

    async def walletcmd(self, message: telethon.tl.types.Message):
        """Отправляет команду /wallet в @send"""
        bot_username = "@send"

        async with message.client.conversation(bot_username) as conv:
            sent_message = await conv.send_message("/wallet")
            response = await conv.get_response()

            await sent_message.delete()
            await response.delete()

        await utils.answer(message, response.text)
