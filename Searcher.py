# meta developer: @shiningwhore
# author: Не знаю, чья идея. Если есть претензии ко мне — канал из meta developer к вашим услугам.

from .. import loader, utils
from telethon import Button

class SearcherMod(loader.Module):
    """Модуль для поиска в различных поисковых системах"""
    strings = {"name": "Searcher"}

    async def searchcmd(self, message):
        """Поиск по запросу в различных системах"""
        query = utils.get_args_raw(message) or (await message.get_reply_message()).raw_text
        if not query:
            await utils.answer(message, "Нужно указать запрос или ответить на сообщение.")
            return

        query_encoded = utils.escape_html(query).replace(' ', '+')

        search_engines = {
            "Google": f"https://www.google.com/search?q={query_encoded}",
            "Bing": f"https://www.bing.com/search?q={query_encoded}",
            "DuckDuckGo": f"https://duckduckgo.com/?q={query_encoded}",
            "Yahoo": f"https://search.yahoo.com/search?p={query_encoded}",
            "Yandex": f"https://yandex.com/search/?text={query_encoded}"
        }

        buttons = [
            [Button.url(name, url)] for name, url in search_engines.items()
        ]

        await message.reply(f"🔍 Links for your request: <code>{utils.escape_html(query)}</code>", buttons=buttons)
