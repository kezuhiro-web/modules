# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods, @shiningwhore

from .. import loader, utils
import os
import yt_dlp

class VideoDownloaderMod(loader.Module):
    """Модуль для скачивания видео с YouTube и TikTok по ссылке"""
    strings = {"name": "VideoDownloader"}

    async def client_ready(self, client, db):
        self.client = client

    async def ytdlcmd(self, message):
        """Скачивает видео с YouTube: .ytdl <ссылка на видео>"""
        args = utils.get_args_raw(message)

        if not args:
            await message.edit("<b>Пожалуйста, укажите ссылку на видео с YouTube!</b>")
            return

        await message.edit("<b>Начинаю загрузку видео с YouTube...</b>")
        await self.download_video(args, message, "youtube")

    async def ttdlcmd(self, message):
        """Скачивает видео из TikTok: .ttdl <ссылка на видео>"""
        args = utils.get_args_raw(message)

        if not args:
            await message.edit("<b>Пожалуйста, укажите ссылку на видео из TikTok!</b>")
            return

        await message.edit("<b>Начинаю загрузку видео из TikTok...</b>")
        await self.download_video(args, message, "tiktok")

    async def download_video(self, url, message, platform):
        """Скачивает видео с указанной платформы (YouTube или TikTok)"""
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # Скачивание в папку downloads
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                video_info = ydl.extract_info(url, download=False)
                video_title = ydl.prepare_filename(video_info)

            await self.client.send_file(message.chat_id, video_title)
            await message.delete()
          
            os.remove(video_title)
        except Exception as e:
            await message.edit(f"<b>Ошибка загрузки видео:</b> {e}")
