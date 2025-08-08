#      РАЗРАБОТЧИК МОДУЛЯ t.me/squeeare
# tg: @squeeare,dc: roze_tka, github: hate11f3

import requests
from .. import loader, utils
import hashlib
import os

@loader.tds
class VirusTotalScan(loader.Module):
    """Проверка файлов и ссылок через VirusTotal"""
    strings = {"name": "VirusTotal"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("vt_api", None, lambda: "🔐 API ключ VirusTotal")
        )

    @loader.command(help="Проверяет файл или ссылку через VirusTotal")
    async def check(self, m):
        api_key = self.config["vt_api"]
        if not api_key:
            return await utils.answer(m, "<b>❌ Укажи API ключ через .cfg vt_api</b>")

        reply = await m.get_reply_message()
        if not reply or not (reply.file or reply.text):
            return await utils.answer(m, "<b>❌ И что же ты собрался проверять? </b>")

        await utils.answer(m, "<b>Проверка. Ждите результат🤗</b>")

        if reply.file:
            path = await reply.download_media()
            with open(path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            os.remove(path)
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        else:
            url_text = reply.raw_text.strip()
            url_id = hashlib.sha256(url_text.encode()).hexdigest()
            url = f"https://www.virustotal.com/api/v3/urls/{url_id}"

        headers = {
            "x-apikey": api_key
        }

        r = requests.get(url, headers=headers)
        if r.status_code == 404:
            return await utils.answer(m, "<b>❌ Нет результатов? Попробуйте снова. </b>")
        elif r.status_code != 200:
            return await utils.answer(m, f"<b>Ошибка: {r.status_code}</b>")

        data = r.json()
        stats = data["data"]["attributes"]["last_analysis_stats"]
        results = data["data"]["attributes"]["last_analysis_results"]

        text = f"<b>🧪 Итог проверки:</b>\n"
        text += f"✅ Чисто: <code>{stats.get('harmless', 0)}</code>\n"
        text += f"❗ Подозрительно: <code>{stats.get('suspicious', 0)}</code>\n"
        text += f"☣️ Опасно: <code>{stats.get('malicious', 0)}</code>\n"
        text += f"💤 Не обнаружено: <code>{stats.get('undetected', 0)}</code>\n\n"

        for engine, result in results.items():
            if result["category"] != "undetected":
                text += f"{engine}: {result['result']}\n"

        if len(text) > 500:
            filename = "vt_result.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text.replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", ""))
            await m.client.send_file(m.chat_id, filename, caption="📄 Результат")
            os.remove(filename)
        else:
            await utils.answer(m, text)