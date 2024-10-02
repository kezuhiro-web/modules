# meta developer: @htmIpage
from .. import loader, utils
import subprocess
import traceback

class SimpleSpeedtestMod(loader.Module):
    strings = {"name": "SimpleSpeedtest"}

    async def speedtestcmd(self, message):
        """Запускает тест скорости интернета"""
        await utils.answer(message, "<b>Замеряю скорость интернета...</b>")
        try:
            result = subprocess.run(["speedtest", "--simple"], capture_output=True, text=True)
            if result.returncode != 0:
                await utils.answer(message, f"<b>Произошла ошибка при выполнении speedtest:</b> {result.stderr}")
            else:
                await utils.answer(message, f"<b>Результат Speedtest'a:</b>\n<pre>{result.stdout}</pre>")
        except Exception:
            await utils.answer(message, f"<b>Произошла ошибка:</b>\n<pre>{traceback.format_exc()}</pre>")
