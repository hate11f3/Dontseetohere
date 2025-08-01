#FILENAME: countme.py
#CLASSNAME: CountMeMod
from .. import loader, utils

@loader.tds
class CountMeMod(loader.Module):
    """Считает ваши сообщения в чате"""
    strings = {"name": "CountMe"}

    @loader.command(ru_doc="Посчитать ваши сообщения в текущем чате")
    async def countme(self, message):
        """Counts your messages in the current chat"""
        await utils.answer(message, "<b>[CountMe]</b> Считаю...")
        count = (await self.client.get_messages(message.chat_id, from_user="me")).total
        await utils.answer(
            message,
            f"<b>[CountMe]</b> В этом чате у вас <code>{count}</code> сообщений.",
        )