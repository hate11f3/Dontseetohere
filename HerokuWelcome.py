from .. import loader, utils
from telethon import events

class HWelcome(loader.Module):
    strings = {"name": "HWelcome"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "WText",
            "Привет, {mention}! Добро пожаловать в {chat} 🎉\n"
            "Какие есть переменные?: {name}, {mention}, {chat}",
            "Текст приветствия (Переменные: {name}, {mention}, {chat})"
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    def is_enabled(self, chat_id):
        return self.db.get(self.strings["name"], str(chat_id), False)

    def set_enabled(self, chat_id, value):
        self.db.set(self.strings["name"], str(chat_id), value)

    @loader.command()
    async def on(self, message):
        self.set_enabled(message.chat_id, True)
        await message.edit("Приветствия в этом чате включены!🤗")

    @loader.command()
    async def off(self, message):
        self.set_enabled(message.chat_id, False)
        await message.edit("Приветствия в этом чате отключены!😭")

    async def watcher(self, message):
        if not (getattr(message, "user_joined", False) or getattr(message, "user_added", False)):
            return
        if not message.chat:
            return
        if not self.is_enabled(message.chat_id):
            return

        for user in message.users:
            if user.is_self:
                continue
            name = user.first_name or "гость"
            mention = f"<a href='tg://user?id={user.id}'>{name}</a>"
            text = self.config["WText"].format(
                name=name,
                chat=message.chat.title,
                mention=mention
            )
            await message.respond(text)

#модуль был сделан @squeeare 
