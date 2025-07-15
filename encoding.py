from .. import loader, utils
import aiohttp
import chardet
import os

@loader.tds
class EncodingFixer(loader.Module):
    strings = {"name": "EncodingFixer"}

    @loader.command()
    async def checkenc(self, message):
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            await message.edit("⚠️ Ответь на файл для проверки.")
            return

        path = await reply.download_media(file="./")
        with open(path, "rb") as f:
            raw = f.read()
        enc = chardet.detect(raw)['encoding']

        await message.edit(f"📑 Кодировка файла: `{enc}`")

    @loader.command()
    async def fixenc(self, message):
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            await message.edit("⚠️ Ответь на файл для перекодировки.")
            return

        path = await reply.download_media(file="./")
        with open(path, "rb") as f:
            raw = f.read()
        enc = chardet.detect(raw)['encoding']

        if enc.lower() == "utf-8":
            await message.edit("✔️ Файл уже в UTF-8.")
            os.remove(path)
            return

        try:
            text = raw.decode(enc)
        except Exception:
            try:
                text = raw.decode(enc, errors='ignore')
            except Exception as e:
                await message.edit(f"❌ Не удалось декодировать: {e}")
                os.remove(path)
                return

        new_path = path + "_utf8.txt"
        with open(new_path, "w", encoding="utf-8") as f:
            f.write(text)

        await message.client.send_file(message.chat_id, new_path, caption=f"✅ Перекодировал из {enc} в UTF-8.")
        await message.delete()
        os.remove(path)
        os.remove(new_path)
