from telethon.tl.types import Message
from .. import loader, utils
import requests
import base64

@loader.tds
class GitHubUploaderMod(loader.Module):
    """Загрузка файлов в репозиторий GitHub по реплаю"""

    strings = {
        "name": "GitHubUploader",
        "no_reply": "❌ Ответь на файл, который хочешь загрузить на GitHub.",
        "uploading": "⏳ Загружаю файл на GitHub...",
        "done": "✅ Загружено: {}",
        "error": "❌ Ошибка загрузки: {}"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "github_token",
                None,
                "GitHub токен. Получить можно тут: https://github.com/settings/tokens",
                validator=loader.validators.Hidden()
            ),
            loader.ConfigValue(
                "github_repo",
                "user/repo",
                "Формат: username/reponame"
            ),
            loader.ConfigValue(
                "github_path",
                "",
                "Путь в репозитории (например: `folder/`). Оставь пустым для корня."
            ),
            loader.ConfigValue(
                "github_branch",
                "main",
                "Ветка для загрузки файлов"
            )
        )

    @loader.command()
    async def gitupload(self, message: Message):
        """Загружает файл с реплая в указанный репозиторий GitHub"""
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
        data = {
            "message": f"Upload {filename}",
            "content": content,
            "branch": branch
        }

        r = requests.put(url, headers=headers, json=data)

        if r.status_code in (200, 201):
            file_url = r.json()["content"]["html_url"]
            await utils.answer(message, self.strings("done").format(file_url))
        else:
            error_msg = r.json().get("message", "Неизвестная ошибка")
            await utils.answer(message, self.strings("error").format(error_msg))
#модуль @squeeare