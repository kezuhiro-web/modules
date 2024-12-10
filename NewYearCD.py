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

from .. import loader, utils
from datetime import datetime, timedelta

@loader.tds
class NewYearCDMod(loader.Module):
    strings = {
        "name": "NewYearCD",
        "countdown": "🎆 <b>Until New Year:</b>\n⏳ <i>{days} {days_text}, {hours} {hours_text}, {minutes} {minutes_text}, {seconds} {seconds_text}!</i>",
        "config_timezone": "☁️ Specify timezone in the format +3, -5, etc.",
        "invalid_timezone": "❌ Invalid timezone format. Specify in format +3, -5, etc.",
        "day": "day",
        "day1": "days",
        "day2": "days",
        "hour": "hour",
        "hour1": "hours",
        "hour2": "hours",
        "minute": "minute",
        "minute1": "minutes",
        "minute2": "minutes",
        "second": "second",
        "second1": "seconds",
        "second2": "seconds",
    }
    
    strings_ru = {
        "countdown": "🎆 <b>До Нового года:</b>\n⏳ <i>{days} {days_text}, {hours} {hours_text}, {minutes} {minutes_text}, {seconds} {seconds_text}!</i>",
        "config_timezone": "☁️ Укажите часовой пояс в формате +3, -5 и т. д.",
        "invalid_timezone": "❌ Неверный формат часового пояса. Укажите в формате +3, -5 и т. д.",
        "day": "день",
        "day1": "дня",
        "day2": "дней",
        "hour": "час",
        "hour1": "часа",
        "hour2": "часов",
        "minute": "минута",
        "minute1": "минуты",
        "minute2": "минут",
        "second": "секунда",
        "second1": "секунды",
        "second2": "секунд",
    }
    def __init__(self):
        self.config = loader.ModuleConfig(
            "TIMEZONE", 0, lambda: self.strings("config_timezone"),
        )

    def format_units(self, value, forms):
        if 11 <= value % 100 <= 19:
            return forms[2]
        elif value % 10 == 1:
            return forms[0]
        elif 2 <= value % 10 <= 4:
            return forms[1]
        else:
            return forms[2]
    
    @loader.command(ru_doc="- Показывает время до Нового Года 🎉")
    async def nycmd(self, message):
        """- Shows time until The New Year 🎉"""
        timezone_offset = self.config["TIMEZONE"]

        if not isinstance(timezone_offset, int) or not (-12 <= timezone_offset <= 14):
            await utils.answer(message, self.strings("invalid_timezone"))
            return

        now = datetime.utcnow() + timedelta(hours=timezone_offset)
        new_year = datetime(now.year + 1, 1, 1)
        delta = new_year - now

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        days_text = self.format_units(days, [self.strings("day"), self.strings("day1"), self.strings("day2")])
        hours_text = self.format_units(hours, [self.strings("hour"), self.strings("hour1"), self.strings("hour2")])
        minutes_text = self.format_units(minutes, [self.strings("minute"), self.strings("minute1"), self.strings("minute2")])
        seconds_text = self.format_units(seconds, [self.strings("second"), self.strings("second1"), self.strings("second2")])

        await utils.answer(
            message,
            self.strings("countdown").format(
                days=days, days_text=days_text,
                hours=hours, hours_text=hours_text,
                minutes=minutes, minutes_text=minutes_text,
                seconds=seconds, seconds_text=seconds_text
            )
        )