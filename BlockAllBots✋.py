from .. import loader, utils
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.types import User
import asyncio

class BlockAllBots(loader.Module):
    strings = {"name": "BlockAllBots"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def blockallbot(self, message):
        await message.edit("Ищу ботов в твоих диалогах...")
        count = 0

        async for dialog in self.client.iter_dialogs():
            entity = dialog.entity
            if isinstance(entity, User) and entity.bot:
                try:
                    await self.client(BlockRequest(entity.id))
                    await self.client(DeleteHistoryRequest(peer=entity.id, max_id=0, revoke=True))
                    count += 1
                    await asyncio.sleep(0.3)
                except Exception as e:
                    await message.respond(f" Не смог заблокировать @{entity.username or entity.first_name}: {e}😥")

        await message.edit(f"Готово! Заблокировано и удалено {count} ботов.🤗")

#модуль был сделан @squeeare 