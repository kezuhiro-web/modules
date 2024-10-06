# meta developer: @htmIpage

import requests
from .. import loader, utils

class GPT4oMMod(loader.Module):
    """Based on docs.onlysq.com"""
    strings = {"name": "GPT4oM"}

    async def client_ready(self, client, db):
        self.client = client

    async def gpt4cmd(self, message):
        """Спросить GPT-4o mini"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>Укажите вопрос!</b>")
            return

        await utils.answer(message, "<b>Спрашиваю GPT-4o mini...</b>")
        
        payload = {
            "model": "gpt-4o-mini",
            "request": {
                "messages": [
                    {
                        "role": "user",
                        "content": args
                    }
                ]
            }
        }

        try:
            response = requests.post('http://api.onlysq.ru/ai/v2', json=payload)
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer", "Ответ не получен.")
            await utils.answer(message, f"<b>Запрос:</b>\n<code>{args}</code>\n\n<b>Ответ GPT-4o mini:</b>\n<code>{answer}</code>")

        except requests.exceptions.RequestException as e:
            await utils.answer(message, f"<b>Произошла ошибка при запросе:</b> {str(e)}")
