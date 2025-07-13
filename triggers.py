from .. import loader, utils
import re

@loader.tds
class TriggersMod(loader.Module):
    """Триггеры на сообщения (можно добавить фото)"""
    strings = {
        "name": "Triggers",
        "chat_enabled": "✅ Триггеры включены",
        "chat_disabled": "❌ Триггеры отключены",
        "chat_status": "🔄 {}",
        "need_reply": "❌ Ответь на сообщение для создания триггера. Например чтобы добавить триггер который на слово <b>привет</b> будет отвечать <b>Привет как дела</b>, то напиши сообщение <code>Привет как дела</code> и на него ответь командой <code>trigadd привет</code>",
        "trigger_added": "✅ Триггер <code>{}</code> добавлен (ID: <code>{}</code>)",
        "trigger_exists": "⚠️ Триггер <code>{}</code> уже есть",
        "trigger_deleted": "✅ Триггер с ID <code>{}</code> удалён",
        "trigger_not_found": "❌ Триггер с ID <code>{}</code> не найден",
        "mode_changed": "✅ Режим триггеров изменён на: {}",
        "trigger_list": "📋 Список триггеров ({}):\n\n{}\n\n🔒 - Строгий режим\n🔍 - Частичный режим\n\nℹ️ Изменение режима триггера невозможно, смена режима действует только на новые триггеры.",
        "no_triggers": "ℹ️ В этом чате нет триггеров",
        "mode_menu": "🔧 Выберите режим работы триггеров:\n\n🔒 Строгий - Срабатывает только при точном совпадении фразы или слова\n\n🔍 Частичный - Срабатывает при наличии слова/фразы в тексте",
        "strict_mode": "Строгий",
        "partial_mode": "Частичный",
        "strict_desc": "Срабатывает только при точном совпадении фразы",
        "partial_desc": "Срабатывает при наличии фразы в тексте",
        "banned": "✅ Пользователь добавлен в чёрный список триггеров",
        "unbanned": "✅ Пользователь убран из чёрного списка триггеров",
        "already_banned": "⚠️ Пользователь уже в чёрном списке",
        "not_banned": "⚠️ Пользователя нет в чёрном списке",
        "ban_list": "📋 Чёрный список триггеров:\n\n{}",
        "empty_ban_list": "ℹ️ Чёрный список триггеров пуст",
    }

    def __init__(self):
        self.db = None
        self.triggers = {}
        self.modes = {}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.triggers = self.db.get("Triggers", "triggers", {}) or {}
        self.modes = self.db.get("Triggers", "modes", {}) or {}

    async def trigchatcmd(self, message):
        """Включить/выключить триггеры в текущем чате"""
        chat_id = str(message.chat_id)
        chats = self.db.get("Triggers", "chats", {}) or {}
        new_status = not chats.get(chat_id, False)
        chats[chat_id] = new_status
        self.db.set("Triggers", "chats", chats)
        status_text = self.strings["chat_enabled"] if new_status else self.strings["chat_disabled"]
        await utils.answer(message, self.strings["chat_status"].format(status_text))

    async def trigaddcmd(self, message):
        """Добавить триггер (в ответ на сообщение, которое будет являться ответом).Например чтобы добавить триггер который на слово 'привет' будет отвечать 'Привет как дела', то напиши сообщение 'Привет как дела' и на него ответь командой trigadd привет"""
        if not message.is_reply:
            await utils.answer(message, self.strings["need_reply"])
            return
        chat_id = str(message.chat_id)
        trigger_name = utils.get_args_raw(message).lower().strip()
        reply_msg = await message.get_reply_message()
        
        if chat_id not in self.triggers:
            self.triggers[chat_id] = {}
        if trigger_name in self.triggers[chat_id]:
            await utils.answer(message, self.strings["trigger_exists"].format(trigger_name))
            return
        
        trigger_id = len(self.triggers[chat_id]) + 1
        data = {
            "id": trigger_id, 
            "mode": self.modes.get(str(message.sender_id), "strict"),
            "chat_id": reply_msg.chat_id,
            "message_id": reply_msg.id
        }
        
        self.triggers[chat_id][trigger_name] = data
        self.db.set("Triggers", "triggers", self.triggers)
        await utils.answer(message, self.strings["trigger_added"].format(trigger_name, trigger_id))

    async def trigmodecmd(self, message):
        """Изменить режим работы триггеров"""
        user_id = str(message.sender_id)
        current_mode = self.modes.get(user_id, "strict")

        def btn_text(mode_key):
            check = "✅ " if mode_key == current_mode else ""
            return f"{check}{self.strings[mode_key + '_mode']}"

        await self.inline.form(
            message=message,
            text=self.strings["mode_menu"],
            reply_markup=[
                [{
                    "text": btn_text("strict"),
                    "callback": self.set_mode,
                    "args": ("strict",),
                    "description": self.strings["strict_desc"]
                }],
                [{
                    "text": btn_text("partial"),
                    "callback": self.set_mode,
                    "args": ("partial",),
                    "description": self.strings["partial_desc"]
                }]
            ],
            silent=True
        )

    async def set_mode(self, call, mode):
        user_id = str(call.from_user.id)
        self.modes[user_id] = mode
        self.db.set("Triggers", "modes", self.modes)

        def btn_text(mode_key):
            check = "✅ " if mode_key == mode else ""
            return f"{check}{self.strings[mode_key + '_mode']}"

        await call.edit(
            self.strings["mode_menu"],
            reply_markup=[
                [{
                    "text": btn_text("strict"),
                    "callback": self.set_mode,
                    "args": ("strict",),
                    "description": self.strings["strict_desc"]
                }],
                [{
                    "text": btn_text("partial"),
                    "callback": self.set_mode,
                    "args": ("partial",),
                    "description": self.strings["partial_desc"]
                }]
            ]
        )
        await call.answer(self.strings["mode_changed"].format(
            self.strings["strict_mode"] if mode == "strict" else self.strings["partial_mode"]), show_alert=False)

    async def trigdelcmd(self, message):
        """Удалить триггер по ID"""
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            await utils.answer(message, "❌ Укажите ID триггера для удаления")
            return
        trigger_id = int(args)
        chat_id = str(message.chat_id)
        if chat_id not in self.triggers or not self.triggers[chat_id]:
            await utils.answer(message, self.strings["no_triggers"])
            return
        deleted = False
        for trigger_name, data in list(self.triggers[chat_id].items()):
            if data["id"] == trigger_id:
                del self.triggers[chat_id][trigger_name]
                deleted = True
                break
        if deleted:
            for idx, (_, data) in enumerate(self.triggers[chat_id].items(), 1):
                data["id"] = idx
            self.db.set("Triggers", "triggers", self.triggers)
            await utils.answer(message, self.strings["trigger_deleted"].format(trigger_id))
        else:
            await utils.answer(message, self.strings["trigger_not_found"].format(trigger_id))

    def get_media_emoji(self, media):
        """Получить эмодзи для типа медиа"""
        if not media:
            return ""
            
        if hasattr(media, 'photo') or str(type(media)).find('Photo') != -1:
            return "[📷]"
        elif hasattr(media, 'video') or str(type(media)).find('Video') != -1:
            return "[🎬]"
        elif hasattr(media, 'document') or str(type(media)).find('Document') != -1:
            if hasattr(media, 'mime_type'):
                mime = media.mime_type
                if mime.startswith('audio/'):
                    return "[🎵]"
                elif mime.startswith('video/'):
                    return "[🎬]"
                elif 'sticker' in mime or mime == 'application/x-tgsticker':
                    return "[🎪]"
                else:
                    return "[📎]"
            else:
                return "[📎]"
        elif hasattr(media, 'voice') or str(type(media)).find('Voice') != -1:
            return "[🎤]"
        elif hasattr(media, 'sticker') or str(type(media)).find('Sticker') != -1:
            return "[🎪]"
        else:
            return "[📎]"

    async def triglistcmd(self, message):
        """Показать список всех триггеров"""
        chat_id = str(message.chat_id)
        if chat_id not in self.triggers or not self.triggers[chat_id]:
            await utils.answer(message, self.strings["no_triggers"])
            return
        triggers = self.triggers[chat_id]
        count = len(triggers)
        trigger_list = []
        for trigger_name, data in triggers.items():
            mode = "🔒" if data["mode"] == "strict" else "🔍"
            preview = ""
            try:
                
                msg = await self.client.get_messages(int(data["chat_id"]), ids=data["message_id"])
                if msg.media:
                    preview += self.get_media_emoji(msg.media)
                    if msg.raw_text:
                        text_preview = msg.raw_text[:30]
                        if len(msg.raw_text) > 30:
                            text_preview += "..."
                        preview += f" {text_preview}"
                else:
                    if msg.raw_text:
                        text_preview = msg.raw_text[:30]
                        if len(msg.raw_text) > 30:
                            text_preview += "..."
                        preview = text_preview
            except:
                preview = "[сообщение недоступно]"
            
            trigger_list.append(
                f"{data['id']}. {mode} <code>{trigger_name}</code> → {preview}"
            )
        await utils.answer(message, self.strings["trigger_list"].format(count, "\n".join(trigger_list)))

    async def trigbancmd(self, message):
        """Заблокировать пользователя для триггеров"""
        if message.is_reply:
            reply_msg = await message.get_reply_message()
            user_id = reply_msg.sender_id
        else:
            args = utils.get_args_raw(message)
            if not args or not args.isdigit():
                await utils.answer(message, "❌ Укажите ID пользователя или ответьте на сообщение")
                return
            user_id = int(args)
        
        blacklist = self.db.get("Triggers", "blacklist", []) or []
        if user_id in blacklist:
            await utils.answer(message, self.strings["already_banned"])
            return
        
        blacklist.append(user_id)
        self.db.set("Triggers", "blacklist", blacklist)
        await utils.answer(message, self.strings["banned"])

    async def trigunbancmd(self, message):
        """Разблокировать пользователя для триггеров"""
        if message.is_reply:
            reply_msg = await message.get_reply_message()
            user_id = reply_msg.sender_id
        else:
            args = utils.get_args_raw(message)
            if not args or not args.isdigit():
                await utils.answer(message, "❌ Укажите ID пользователя или ответьте на сообщение")
                return
            user_id = int(args)
        
        blacklist = self.db.get("Triggers", "blacklist", []) or []
        if user_id not in blacklist:
            await utils.answer(message, self.strings["not_banned"])
            return
        
        blacklist.remove(user_id)
        self.db.set("Triggers", "blacklist", blacklist)
        await utils.answer(message, self.strings["unbanned"])

    async def trigbanlistcmd(self, message):
        """Показать чёрный список триггеров"""
        blacklist = self.db.get("Triggers", "blacklist", []) or []
        if not blacklist:
            await utils.answer(message, self.strings["empty_ban_list"])
            return
        
        ban_list = []
        for user_id in blacklist:
            try:
                user = await self.client.get_entity(user_id)
                name = user.first_name
                if user.last_name:
                    name += f" {user.last_name}"
                ban_list.append(f"{name} (<code>{user_id}</code>)")
            except:
                ban_list.append(f"Пользователь <code>{user_id}</code>")
        
        await utils.answer(message, self.strings["ban_list"].format("\n".join(ban_list)))

    async def watcher(self, message):
        if not message.text:
            return
        chat_id = str(message.chat_id)
        chats = self.db.get("Triggers", "chats", {}) or {}
        if not chats.get(chat_id, False):
            return
        if chat_id not in self.triggers or not self.triggers[chat_id]:
            return
        blacklist = self.db.get("Triggers", "blacklist", []) or []
        if message.sender_id in blacklist:
            return
        
        text = message.text.lower()
        for trigger_name, data in self.triggers[chat_id].items():
            match = False
            if data["mode"] == "strict":
                
                if text.strip() == trigger_name.strip():
                    match = True
            else:
                if trigger_name in text:
                    match = True
            if match:
                try:
                    
                    original_msg = await self.client.get_messages(int(data["chat_id"]), ids=data["message_id"])
                    
                    
                    await self.client.send_message(
                        message.chat_id,
                        original_msg.message or "",
                        reply_to=message.id,
                        file=original_msg.media
                    )
                    
                except Exception as e:
                    
                    error_info = f"❌ Ошибка триггера '{trigger_name}':\n"
                    error_info += f"Сохранённый chat_id: {data.get('chat_id', 'НЕ НАЙДЕН')}\n"
                    error_info += f"Сохранённый message_id: {data.get('message_id', 'НЕ НАЙДЕН')}\n"
                    error_info += f"Ошибка: {str(e)}"
                    await message.reply(error_info)
                break