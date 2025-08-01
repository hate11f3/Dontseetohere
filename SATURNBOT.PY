import random
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.enums import ChatType
from aiogram.utils.markdown import hbold

API_TOKEN = '8386869957:AAFPym7-_DALQR_niujgxf-JOTBz81vFl0M'  # Ваш токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Хранилище для IQ тестов и предупреждений
active_iq_tests = {}  # user_id: правильный ответ
warns = {}            # user_id: количество предупреждений

rules_text = "Стандартные правила группы."

# Проверка, является ли пользователь админом
async def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.is_chat_admin()
    except Exception:
        return False

# Генерация IQ задачи для проверки при вступлении
def generate_math_problem():
    level = random.choice(['easy', 'mid', 'hard'])
    if level == 'easy':
        if random.random() < 0.5:
            n = random.choice([4, 9, 16, 25])
            return (f"√{n} = ?", str(int(n**0.5)))
        else:
            a, b = random.randint(50, 300), random.randint(50, 500)
            return (f"{a} + {b} = ?", str(a + b))
    elif level == 'mid':
        a, b = random.randint(7, 21), random.randint(2, 12)
        if random.random() < 0.5:
            return (f"{a} × {b} = ?", str(a * b))
        else:
            c = random.randint(10, 80)
            return (f"x + {a} = {c}. Чему равен x?", str(c - a))
    else:
        # Сложная задача-ловушка для роботов
        return (
            "Вычислите производную по x:\n"
            "y = (6A + 4B)cos(3x) + (4A - 6B)sin(3x) + x((-5A)sin(3x) + (12A - 5B)cos(3x)) + (25A sin(3x) + 25B cos(x))\n"
            "Ответ: Невозможно решить без значений A и B",
            "Невозможно решить без значений A и B"
        )

# Обработка запроса на вступление с IQ-тестом
@dp.chat_join_request()
async def on_join_request(event: types.ChatJoinRequest):
    question, answer = generate_math_problem()
    active_iq_tests[event.from_user.id] = answer
    await bot.send_message(
        event.from_user.id,
        f"Для входа в чат решите задачу:\n\n{question}\n\nОтвет пришлите одним сообщением."
    )
    # Заявка на вступление не одобряется пока не решит задачу

# Обработка ответов на IQ тесты
@dp.message()
async def handle_iq_answer(message: types.Message):
    user_id = message.from_user.id
    if user_id in active_iq_tests:
        correct = active_iq_tests[user_id]
        if message.text.strip() == correct:
            del active_iq_tests[user_id]
            # Одобряем заявку на вступление
            join_requests = await bot.get_chat_join_requests(message.chat.id)
            approved = False
            for req in join_requests:
                if req.from_user.id == user_id:
                    await bot.approve_chat_join_request(message.chat.id, user_id)
                    await bot.send_message(user_id, "✅ Верно! Добро пожаловать в чат.")
                    approved = True
                    break
            if not approved:
                await message.answer("❗ Заявка на вступление не найдена, попробуйте позже.")
        else:
            await message.reply("❌ Неверный ответ, попробуйте ещё раз.")

# Команда помощи
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "/ban <время> (в ответ на сообщение) – забанить пользователя\n"
        "/unban (в ответ на сообщение) – снять бан\n"
        "/mute <время> (в ответ на сообщение) – замутить пользователя\n"
        "/warn (в ответ на сообщение) – выдать предупреждение\n"
        "/kick (в ответ на сообщение) – кикнуть пользователя\n"
        "/rules – показать правила\n"
        "/setrules <текст> – изменить правила (только админы)\n"
        "/admins – список админов\n"
        "/help – показать эту помощь"
    )
    await message.answer(help_text)

# Команда для отображения админов
@dp.message(Command("admins"))
async def cmd_admins(message: types.Message):
    admins = await bot.get_chat_administrators(message.chat.id)
    text = "Список админов:\n"
    for adm in admins:
        user = adm.user
        text += f"• {hbold(user.full_name)} (@{user.username or user.id})\n"
    await message.answer(text)

# Показываем правила
@dp.message(Command("rules"))
async def cmd_rules(message: types.Message):
    await message.answer(rules_text)

# Меняем правила
@dp.message(Command("setrules"))
async def cmd_setrules(message: types.Message, command: CommandObject):
    if await is_admin(message.chat.id, message.from_user.id):
        global rules_text
        rules_text = command.args.strip()
        await message.answer("Новые правила сохранены.")
    else:
        await message.reply("Только администраторы могут менять правила.")

# Бан с возможностью указать время (например: 10m, 1h)
@dp.message(Command("ban"))
async def cmd_ban(message: types.Message, command: CommandObject):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply("Только админы могут использовать эту команду.")
        return
    if not message.reply_to_message:
        await message.reply("Используйте команду в ответ на сообщение пользователя.")
        return
    user_id = message.reply_to_message.from_user.id
    time_arg = command.args.strip().lower()
    until = None
    if time_arg:
        try:
            if time_arg.endswith("s"):
                seconds = int(time_arg[:-1])
                until = datetime.utcnow() + timedelta(seconds=seconds)
            elif time_arg.endswith("m"):
                minutes = int(time_arg[:-1])
                until = datetime.utcnow() + timedelta(minutes=minutes)
            elif time_arg.endswith("h"):
                hours = int(time_arg[:-1])
                until = datetime.utcnow() + timedelta(hours=hours)
        except Exception:
            pass
    await bot.ban_chat_member(message.chat.id, user_id, until_date=until)
    await message.reply(f"Пользователь забанен{' до ' + str(until) if until else ' навсегда'}.")

# Досрочный разбан
@dp.message(Command("unban"))
async def cmd_unban(message: types.Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply("Только админы могут использовать эту команду.")
        return
    if not message.reply_to_message:
        await message.reply("Используйте команду в ответ на сообщение пользователя.")
        return
    user_id = message.reply_to_message.from_user.id
    await bot.unban_chat_member(message.chat.id, user_id, only_if_banned=True)
    await message.reply("Пользователь успешно разбанен.")

# Мут с временем (например: 10m, 1h)
@dp.message(Command("mute"))
async def cmd_mute(message: types.Message, command: CommandObject):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply("Только админы могут использовать эту команду.")
        return
    if not message.reply_to_message:
        await message.reply("Используйте команду в ответ на сообщение пользователя.")
        return
    user_id = message.reply_to_message.from_user.id
    time_arg = command.args.strip().lower()
    until = None
    if time_arg:
        try:
            if time_arg.endswith("s"):
                seconds = int(time_arg[:-1])
                until = datetime.utcnow() + timedelta(seconds=seconds)
            elif time_arg.endswith("m"):
                minutes = int(time_arg[:-1])
                until = datetime.utcnow() + timedelta(minutes=minutes)
            elif time_arg.endswith("h"):
                hours = int(time_arg[:-1])
                until = datetime.utcnow() + timedelta(hours=hours)
        except Exception:
            pass
    # Если время не указано или не распарсилось - 1 час
    if until is None:
        until = datetime.utcnow() + timedelta(hours=1)
    perms = types.ChatPermissions(can_send_messages=False)
    await bot.restrict_chat_member(message.chat.id, user_id, permissions=perms, until_date=until)
    await message.reply(f"Пользователь замьючен до {until} UTC.")

# Кик (бан + разбан для удаления из чата)
@dp.message(Command("kick"))
async def cmd_kick(message: types.Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply("Только админы могут использовать эту команду.")
        return
    if not message.reply_to_message:
        await message.reply("Используйте команду в ответ на сообщение пользователя.")
        return
    user_id = message.reply_to_message.from_user.id
    await bot.ban_chat_member(message.chat.id, user_id)
    await bot.unban_chat_member(message.chat.id, user_id)
    await message.reply("Пользователь кикнут.")

# Выдача предупреждений
@dp.message(Command("warn"))
async def cmd_warn(message: types.Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply("Только админы могут использовать эту команду.")
        return
    if not message.reply_to_message:
        await message.reply("Используйте команду в ответ на сообщение пользователя.")
        return
    user_id = message.reply_to_message.from_user.id
    warns[user_id] = warns.get(user_id, 0) + 1
    count = warns[user_id]
    if count >= 3:
        await message.reply(f"Пользователь получил {count} предупреждения. Рекомендуется кикнуть или отправить на IQ тест повторно.")
    else:
        await message.reply(f"Пользователь получил предупреждение {count}/3.")

# Анти-спам/анти-скам: удаляем ссылки и подозрительные слова от неадминов
@dp.message()
async def anti_spam_filter(message: types.Message):
    if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return
    text_lower = (message.text or "").lower()
    bad_links = ['http://', 'https://', 't.me/', '.me/', '.ru', '.com']
    bad_words = ['scam', 'крипта', 'crypto']
    if any(link in text_lower for link in bad_links) or any(word in text_lower for word in bad_words):
        if not await is_admin(message.chat.id, message.from_user.id):
            try:
                await message.delete()
                await message.answer(f"Пользователь @{message.from_user.username or message.from_user.id} не может отправлять ссылки или подозрительные сообщения.")
            except Exception:
                pass

dp.message.register(anti_spam_filter)

# Запуск бота
def main():
    print("Бот запущен...")
    dp.run_polling()

if __name__ == "__main__":
    main()
