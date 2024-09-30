# meta developer: @shiningwhore
from .. import loader, utils
import subprocess
import traceback

class SimpleSpeedtestMod(loader.Module):
    strings = {"name": "SimpleSpeedtest"}

    async def speedtestcmd(self, message):
        """Запускает тест скорости интернета"""
        await message.edit("Замеряю скорость интернета...")
        try:
            result = subprocess.run(["speedtest", "--simple"], capture_output=True, text=True)
            if result.returncode != 0:
                await message.edit(f"Произошла ошибка при выполнении speedtest: {result.stderr}")
            else:
                await message.edit(f"<b>Результат SpeedTest:</b>\n<pre>{result.stdout}</pre>")
        except Exception:
            await message.edit(f"Произошла ошибка:\n<pre>{traceback.format_exc()}</pre>")
