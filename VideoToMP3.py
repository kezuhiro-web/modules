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
import os
from telethon.tl.types import Message, DocumentAttributeAudio
from moviepy import VideoFileClip

@loader.tds
class VideoToMP3Mod(loader.Module):
    strings = {
        "name": "📷 VideoToMP3",
        "not_reply": "💢 <b>Reply to video for conversion.</b>",
        "conv_msg": "🔄 <b>Converting video to audio...</b>",
        "conv_successful": "✅ <b>Conversion complete!</b>",
        "error": "❎ <b>An error occured:</b>\n<pre><code class='language-python'>{}</code></pre>",
    }
    strings_ru = {
        "not_reply": "💢 <b>Ответьте на видео для конвертации.</b>",
        "conv_msg": "🔄 <b>Конвертация видео в аудио...</b>",
        "conv_successful": "✅ <b>Конвертация завершена!</b>",
        "error": "❎ <b>Произошла ошибка:</b>\n<pre><code class='language-python'>{}</code></pre>",
    }
    
    @loader.command(ru_doc=" <reply_to_video> [имя_файла] - Конвертировать видео в аудио")
    async def mp3cmd(self, message: Message):
        """ <reply_to_video> [file_name] - Convert video to audio"""
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)

        if not reply or not reply.video:
            await utils.answer(message, self.strings("not_reply"))
            return
        
        conv_msg = await utils.answer(message, self.strings("conv_msg"))
        
        video = await reply.download_media()

        try:
            audio_file = f"@dummykezu.mp3"
            video_clip = VideoFileClip(video)
            video_clip.audio.write_audiofile(audio_file)
            video_clip.close()
    
            await conv_msg.delete()
    
            await message.client.send_file(
                message.chat_id,
                audio_file,
                caption=self.strings("conv_successful"),
                attributes=[
                    DocumentAttributeAudio(
                        duration=0,
                        performer="@dummykezu",
                        title=args if args else "Video",
                    )
                ],
                reply_to=reply.id
            )

            os.remove(video)
            os.remove(audio_file)
            
        except Exception as e:
            await utils.answer(message, self.strings("error").format(e))
            
            if os.path.exists(video):
                os.remove(video)
            if os.path.exists(audio_file):
                os.remove(audio_file)
