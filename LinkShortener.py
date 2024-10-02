# meta developer: @htmIpage
# author: Не знаю, чья идея. Если есть претензии ко мне — профиль из meta developer к вашим услугам.

import requests
from .. import loader, utils

@loader.tds
class LinkShortenerMod(loader.Module):
    """Модуль для сокращения ссылок через TinyURL"""
    strings = {"name": "LinkShortener"}

    async def client_ready(self, client, db):
        self.client = client

    async def slinkcmd(self, message):
        """Сокращает ссылку. Использование: .slink <link or reply>"""
        
        args = utils.get_args_raw(message)
        if not args and message.is_reply:
            reply_message = await message.get_reply_message()
            args = reply_message.raw_text
        
        if not args:
            await utils.answer(message, "<b>Пожалуйста, укажите ссылку для сокращения или ответьте на сообщение с ссылкой.</b>")
            return
        
        if not args.startswith("http"):
            await utils.asnwer(message, "<b>Неверная ссылка. Она должна начинаться с http или https.</b>")
            return

        try:
            response = requests.get(f"http://tinyurl.com/api-create.php?url={args}")
            if response.status_code == 200:
                short_url = response.text
                await utils.answer(message, f"<b>Сокращенная ссылка:</b> {short_url}")
            else:
                await utils.answer(message, "<b>Ошибка при сокращении ссылки.</b>")
        except Exception as e:
            await utils.answer(message, f"<b>Произошла ошибка:</b> {str(e)}")
