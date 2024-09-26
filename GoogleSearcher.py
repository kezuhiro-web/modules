#meta developer: @shiningwhore

__version__ = (1, 0, 1)

from .. import loader, utils

@loader.tds
class GoogleSearcherMod(loader.Module):
    """Google Search engine module."""
    strings = {
    "name": "GoogleSearcher",
    }

    async def googlecmd(self, message):
        """ <args> — Create link for your request"""
        
        args = message.message.split(" ")
        
        if not args:
            await message.edit("<b>❌ No args</b>")
        else:
            await message.edit(f"🔎 <b>Link for your request is <a href='https://google.com/search?q={args}'>here</a></b>")
