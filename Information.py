# meta developer: @shiningwhore

from .. import loader, utils
from telethon import types

class InformationMod(loader.Module):
    """Модуль для получения информации о пользователе или чате"""
    strings = {"name": "Information"}

    async def ainfocmd(self, message):
        """Получить информацию о пользователе или чате"""
        if message.is_reply:
            user = await message.get_reply_message()
            target = user.from_id
        else:
            args = utils.get_args_raw(message)
            if not args:
                await utils.answer(message, "Укажите username или ID пользователя.")
                return
            try:
                target = await self.client.get_entity(args)
            except Exception as e:
                await utils.answer(message, f"Ошибка: {str(e)}")
                return

        if isinstance(target, (types.User, types.Bot)):
            name = target.first_name or ""
            last_name = target.last_name or ""
            username = target.username or "None"
            user_id = target.id
            about = getattr(target, 'about', "None")
            avatar = target.photo
            common_groups = await self.get_common_groups(target)

            result_message = f"<b>Name:</b> {name} {last_name}\n<b>Username:</b> {username}\n<b>ID:</b> {user_id}\n<b>Bio:</b> {about}\n<b>Common groups:</b> {common_groups}"

            if avatar:
                avatar_url = await self.client.download_profile_photo(avatar, bytes=True)
                await message.client.send_file(
                    message.chat_id,
                    avatar_url,
                    caption=result_message,
                    parse_mode="html"
                )
            else:
                await utils.answer(message, result_message)

        elif isinstance(target, types.Chat):
            chat_name = target.title
            chat_id = target.id
            chat_link = f"<a href='tg://chat?id={chat_id}'>Link</a>"
            avatar = target.photo

            result_message = f"<b>Chat Name:</b> {chat_name}\n<b>ID:</b> {chat_id}\n<b>Link:</b> {chat_link}"

            if avatar:
                avatar_url = await self.client.download_profile_photo(avatar, bytes=True)
                await message.client.send_file(
                    message.chat_id,
                    avatar_url,
                    caption=result_message,
                    parse_mode="html"
                )
            else:
                await utils.answer(message, result_message)

    async def get_common_groups(self, user):
        """Получить общее количество групп, в которых состоит пользователь"""
        common_chats = await self.client.get_dialogs()
        common_groups = [chat.title for chat in common_chats if chat.is_group and chat.id in user.participation]
        return ", ".join(common_groups) if common_groups else "Нет общих групп."
