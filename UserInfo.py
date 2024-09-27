# meta developer: @shiningwhore
# author: Не знаю, чья идея. Если есть претензии ко мне — канал из meta developer к вашим услугам.

from .. import loader, utils
import telethon

@loader.tds
class UserInfoMod(loader.Module):
    """Получение информации о пользователе"""
    strings = {"name": "UserInfo"}

    async def uinfocmd(self, message):
        """Использование: .uinfo <reply или @username> — Получить информацию о пользователе"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        try:
            if reply:
                user = await message.client.get_entity(reply.sender_id)
            elif args:
                user = await message.client.get_entity(args)
            else:
                user = await message.client.get_entity(message.sender_id)
        except ValueError as e:
            await message.edit(f"Не удалось найти пользователя. Ошибка: {str(e)}")
            return

        photo = await message.client.download_profile_photo(user.id)

        user_info = (
            f"<b>Имя:</b> {utils.escape_html(user.first_name or 'Не указано')}\n"
            f"<b>Фамилия:</b> {utils.escape_html(user.last_name or 'Не указана')}\n"
            f"<b>Юзернейм:</b> @{user.username or 'Не указан'}\n"
            f"<b>ID:</b> {user.id}\n"
            f"<b>Бот:</b> {'Да' if user.bot else 'Нет'}\n"
        )

        if photo:
            await message.client.send_file(message.chat_id, photo, caption=user_info)
            await message.delete()
        else:
            await message.edit(user_info)
