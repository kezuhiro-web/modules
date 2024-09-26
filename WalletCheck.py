# meta developer: @shiningwhore
# author: Не знаю, чья идея. Если есть претензии ко мне — канал из meta developer к вашим услугам.

from .. import loader, utils
import telethon

class CryptoWalletMod(loader.Module):
    """Модуль для взаимодействия с @cryptobot"""
    strings = {'name': 'CryptoWallet'}

    async def walletcmd(self, message: telethon.tl.types.Message):
        """Отправляет команду /wallet в @cryptobot, удаляет её и меняет сообщение команды"""
        bot_username = "@CryptoBot"

        async with message.client.conversation(bot_username) as conv:
            sent_message = await conv.send_message("/wallet")
            response = await conv.get_response()

            await sent_message.delete()

        await message.edit(response.text)
