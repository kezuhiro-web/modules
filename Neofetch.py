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

# meta developer: @dummykezu

import subprocess
import traceback
from .. import loader, utils

@loader.tds
class NeofetchMod(loader.Module):
    strings = {
        "name": "Neofetch",
        "not_installed": "Please, install <i>Neofetch</i>",
    }

    strings_ru = {
        "not_installed": "Пожалуйста, установите <i>Neofetch</i>",
    }

    strings_ua = {
        "not_installed": "Будь ласка, встановіть <i>Neofetch</i>",
    }

    @loader.command(
        ru_doc="- запустить команду neofetch",
        ua_doc="- запустити команду neofetch",
    )
    async def neofetchcmd(self, message):
        """- run neofetch command"""
        try:
            result = subprocess.run(["neofetch", "--stdout"], capture_output=True, text=True)
            output = result.stdout
            await utils.answer(message, f"<pre>{utils.escape_html(output)}</pre>")
            
        except FileNotFoundError:
            await utils.answer(message, self.strings("not_installed"))
