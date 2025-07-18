# meta developer: @squeeare
# meta plugin: githubuploader

from telethon.tl.types import Message
from hikkatl.types import Message
from hikka import loader, utils
import aiohttp
import base64

class GitHubUploaderMod(loader.Module):
    """Загрузка файлов из реплая в GitHub репозиторий"""
    strings = {"name": "GitHubUploader"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "github_token", None,
                lambda: "Токен GitHub с правами доступа к репозиторию (repo)"
                validator=loader.validators.Hidden() # скрой токен из кфг плиз
            ),
            loader.ConfigValue(
                "github_repo", None,
                lambda: "Репозиторий в формате username/repo"
            ),
            loader.ConfigValue(
                "github_branch", "main",
                lambda: "Ветка репозитория (по умолчанию main)"
            ),
        )

    async def gituploadcmd(self, message: Message):
        """[реплай на файл] — загружает файл в репозиторий GitHub"""
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            return await utils.answer(message, "❗ Реплай на файл обязателен.")
        
        file = await reply.download_media(bytes)
        filename = reply.file.name or "uploaded_file"

        token = self.config["github_token"]
        repo = self.config["github_repo"]
        branch = self.config["github_branch"]

        if not token or not repo:
            return await utils.answer(message, "❗ Не настроен токен или репозиторий в конфиге модуля.")

        api_url = f"https://api.github.com/repos/{repo}/contents/{filename}"

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }

        payload = {
            "message": f"Upload {filename}",
            "content": base64.b64encode(file).decode(),
            "branch": branch
        }

        async with aiohttp.ClientSession() as session:
            async with session.put(api_url, headers=headers, json=payload) as resp:
                if resp.status in (200, 201):
                    data = await resp.json()
                    download_url = data.get("content", {}).get("download_url", "")
                    await utils.answer(message, f"✅ Файл загружен: [ссылка]({download_url})")
                else:
                    error = await resp.text()
                    await utils.answer(message, f"❌ Ошибка загрузки:\n{error}")
