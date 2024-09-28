# meta developer: @shiningwhore

import subprocess
import traceback
from .. import loader, utils

@loader.tds
class NeofetchMod(loader.Module):
    strings = {"name": "Neofetch"}

    async def neofetchcmd(self, message):
        """Запустить команду neofetch"""
        try:
            result = subprocess.run(["neofetch", "--stdout"], capture_output=True, text=True)
            output = result.stdout

            if result.returncode != 0:
                await message.edit(f"<b>Ошибка выполнения команды neofetch:</b>\n{result.stderr}")
                return

            await message.edit(f"<pre>{utils.escape_html(output)}</pre>")
        except Exception:
            await message.edit(f"<b>Ошибка:</b>\n<pre>{traceback.format_exc()}</pre>")
