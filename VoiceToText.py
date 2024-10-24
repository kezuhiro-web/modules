# meta developer: @y9_d0lbaeb

from .. import loader, utils
import os
import speech_recognition as sr
from pydub import AudioSegment

@loader.tds
class VoiceToTextMod(loader.Module):
    """Voice and video messages to text translation with auto-recognition"""
    strings = {
        "process_text": "⏳ <b>Recognizing the message text...</b>",
        "vtt_success": "💬 <b>Recognized text:</b>\n<code>{}</code>",
        "vtt_failure": "🚫 <b>Failed to recognize the message.</b>",
        "vtt_request_error": "🚫 <b>Error when contacting the recognition service:</b>\n<code>{}</code>",
        "vtt_invalid": "🚫 <b>Please reply to a voice or video message with the command</b> <code>.vtt</code>"
    }

    strings_ru = {
        "process_text": "⏳ <b>Распознаю текст сообщения...</b>",
        "vtt_success": "💬 <b>Распознанный текст:</b>\n<code>{}</code>",
        "vtt_failure": "🚫 <b>Не удалось распознать сообщение.</b>",
        "vtt_request_error": "🚫 <b>Ошибка при обращении к сервису распознавания:</b>\n<code>{}</code>",
        "vtt_invalid": "🚫 <b>Пожалуйста, ответьте на голосовое или видеосообщение командой</b> <code>.vtt</code>"
    }

    @loader.command(
        ru_doc="Распознает текст из голосового или видеосообщения.",
    )
    async def vttcmd(self, message):
        """Recognizes text from voice or video messages."""
        await self._process_voice_to_text(message)

    async def _process_voice_to_text(self, message, auto=False):
        waiting_message = await utils.answer(
            message, self.strings["process_text"], reply_to=message.id if auto else None
        )
        reply = message if auto else await message.get_reply_message()

        if not reply or not (reply.voice or reply.video_note):
            await waiting_message.delete()
            if not auto:
                await message.respond(self.strings["vtt_invalid"])
            return

        media_file = await reply.download_media()
        wav_file = media_file.replace('.mp4', '.wav') if reply.video_note else media_file.replace('.oga', '.wav')

        try:
            AudioSegment.from_file(media_file).export(wav_file, format='wav')
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_file) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language='ru-RU')
                    await reply.reply(self.strings["vtt_success"].format(text))
                except sr.UnknownValueError:
                    await reply.reply(self.strings["vtt_failure"])
                except sr.RequestError as e:
                    await reply.reply(self.strings["vtt_request_error"].format(e))
        finally:
            await waiting_message.delete()
            os.remove(media_file)
            os.remove(wav_file)
