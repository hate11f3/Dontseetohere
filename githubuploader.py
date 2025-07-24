#.          ___  __ _ _   _  ___  ___  __ _ _ __ ___ 
#          / __|/ _` | | | |/ _ \/ _ \/ _` | '__/ _ \
#          \__ \ (_| | |_| |  __/  __/ (_| | | |  __/
#          |___/\__, |\__,_|\___|\___|\__,_|_|  \___|
#                  |_|                               
#       Всем привет ребята, я squeeare создатель модулей
#.             Надеюсь вам понравится этот модуль
#.    Помогите мне стать оффициальным производителем модулей
#.        .             Буду очень рад :)

from telethon.tl.types import Message
from .. import loader, utils
import requests
import base64

@loader.tds
class GitHubUploaderMod(loader.Module):
    strings = {
        "name": "GitHubUploader",
        "no_reply": "❌ Ответь на файл, который хочешь загрузить на GitHub.",
        "uploading": "⏳ Загружаю файл на GitHub...",
        "done": "✅ Загружено: {}",
        "error": "❌ Ошибка загрузки: {}"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("github_token", None, "", validator=loader.validators.Hidden()),
            loader.ConfigValue("github_repo", "user/repo", ""),
            loader.ConfigValue("github_path", "", ""),
            loader.ConfigValue("github_branch", "main", "")
        )

    @loader.command()
    async def gitupload(self, message: Message):
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            await utils.answer(message, self.strings("no_reply"))
            return

        await utils.answer(message, self.strings("uploading"))

        file = await reply.download_media(bytes)
        filename = reply.file.name or "uploaded_file"

        token = self.config["github_token"]
        repo = self.config["github_repo"]
        path = self.config["github_path"]
        branch = self.config["github_branch"]

        if not token or not repo:
            await utils.answer(message, "❌ Не настроен токен или репозиторий в .cfg")
            return

        full_path = f"{path}{filename}"
        content = base64.b64encode(file).decode()

        url = f"https://api.github.com/repos/{repo}/contents/{full_path}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

        r_get = requests.get(url, headers=headers, params={"ref": branch})
        sha = r_get.json().get("sha") if r_get.status_code == 200 else None

        data = {
            "message": f"{'Update' if sha else 'Upload'} {filename}",
            "content": content,
            "branch": branch
        }

        if sha:
            data["sha"] = sha

        r = requests.put(url, headers=headers, json=data)

        if r.status_code in (200, 201):
            file_url = r.json()["content"]["html_url"]
            await utils.answer(message, self.strings("done").format(file_url))
        else:
            error_msg = r.json().get("message", "Неизвестная ошибка")
            await utils.answer(message, self.strings("error").format(error_msg))