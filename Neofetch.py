#  _  __  ___   ____  _   _ 
# | |/ / | __| |_  / | | | |
# | ' <  | _|   / /  | |_| |
# |_|\_\ |___| /___|  \___/
#
#  __  __    ___    ___    ___ 
# |  \/  |  / _ \  |   \  / __|
# | |\/| | | (_) | | |) | \__ \
# |_|  |_|  \___/  |___/  |___/
#

# meta developer: @biokezu

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
                await utils.answer(message, f"<b>Ошибка выполнения команды neofetch:</b>\n{result.stderr}")
                return

            await utils.answer(message, f"<pre>{utils.escape_html(output)}</pre>")
        except Exception:
            await utils.answer(message, f"<b>Ошибка:</b>\n<pre>{traceback.format_exc()}</pre>")
