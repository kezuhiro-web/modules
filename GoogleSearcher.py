#meta developer: @htmIpage

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
        
        args = utils.get_args_raw()
        
        if not args:
            await utils.answer(message, "<b>❌ No args</b>")
        else:
            await utils.answer(message, f"🔎 <b>Link for your request is <a href='https://google.com/search?q={args}'>here</a></b>")
