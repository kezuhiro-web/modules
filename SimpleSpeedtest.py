# meta developer: @shiningwhore
from .. import loader, utils
import subprocess
import traceback

class SimpleSpeedtestMod(loader.Module):
    strings = {"name": "SimpleSpeedtest"}

    async def speedtestcmd(self, message):
        """Запускает тест скорости интернета"""
        await message.edit("<b>Замеряю скорость интернета...</b>")
        try:
            result = subprocess.run(["speedtest", "--simple"], capture_output=True, text=True)
            if result.returncode != 0:
                await message.edit(f"<b>Произошла ошибка при выполнении speedtest:</b> {result.stderr}")
            else:
                await message.edit(f"<b>Результат Speedtest'a:</b>\n<pre>{result.stdout}</pre>")
        except Exception:
            await message.edit(f"<b>Произошла ошибка:</b>\n<pre>{traceback.format_exc()}</pre>")
