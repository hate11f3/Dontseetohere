# meta developer: @HATEL1F33
# meta plugin: ttsvoice

from .. import loader, utils
from gtts import gTTS
import os

class TTSVoiceMod(loader.Module):
    """Преобразует текст в голосовое сообщение"""
    strings = {"name": "TTSVoice"}

    @loader.command()
    async def tts(self, message):
        """[текст] — озвучить текст голосом"""
        text = utils.get_args_raw(message)
        if not text:
            await message.edit("❌ Укажи текст для озвучки.")
            return

        try:
            tts = gTTS(text, lang='ru')  # привет
            file_path = "voice_message.ogg"
            tts.save(file_path)

            await self.client.send_file(
                message.chat_id,
                file_path,
                voice_note=True,  
                reply_to=message.reply_to_msg_id
            )

            await message.delete()
            os.remove(file_path)

        except Exception as e:
            await message.edit(f"❌ Ошибка: {e}")
