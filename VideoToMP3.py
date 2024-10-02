# meta developer: @htmIpage

from .. import loader, utils
import os
from telethon.tl.types import Message
from moviepy.editor import VideoFileClip

@loader.tds
class VideoToMP3Mod(loader.Module):
    """Модуль для конвертации видео в аудио и сохранения в mp3"""
    strings = {"name": "VideoToMP3"}

    async def mp3cmd(self, message: Message):
        """ <reply_to_video> [название_файла] - Конвертировать видео в аудио и сохранить как MP3"""
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)

        if not reply or not reply.video:
            await utils.answer(message, "<b>Ответьте на видео для конвертации.</b>")
            return

        video = await reply.download_media()
        await utils.answer(message, "<b>Конвертация видео в аудио...</b>")

        try:
            audio_file = f"{args}.mp3" if args else "video.mp3"
            video_clip = VideoFileClip(video)
            video_clip.audio.write_audiofile(audio_file)
            video_clip.close()

            await message.client.send_file(message.chat_id, audio_file, reply_to=reply.id)
            await utils.answer(message, "<b>Конвертация завершена!</b>")

            os.remove(video)
            os.remove(audio_file)
        except Exception as e:
            await utils.answer(message, f"<b>Произошла ошибка: {e}</b>")
            if os.path.exists(video):
                os.remove(video)
            if os.path.exists(audio_file):
                os.remove(audio_file)
