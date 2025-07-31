#FILENAME:quote_of_day.py
#CLASSNAME:QuoteOfDayMod
from .. import loader, utils
import aiohttp


@loader.tds
class QuoteOfDayMod(loader.Module):
    """Модуль для получения случайной цитаты дня."""
    strings = {
        "name": "Quote Of Day",
        "loading": "<b>⏳ Получаю цитату...</b>",
        "api_error": "<b>🚫 Ошибка API. Попробуйте позже.</b>",
        "lang_error": "<b>Поддерживаемые языки: <code>ru</code>, <code>en</code>.</b>",
        "unknown_author": "Неизвестный автор",
    }

    @loader.command(aliases=["qotd"], doc="Получить случайную цитату")
    async def quote(self, message):
        """<lang> - Получить цитату на определенном языке (ru/en). По умолчанию ru."""
        lang = utils.get_args_raw(message) or "ru"
        if lang not in ["ru", "en"]:
            await utils.answer(message, self.strings("lang_error"))
            return

        await utils.answer(message, self.strings("loading"))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={lang}"
                ) as response:
                    if response.status != 200:
                        await utils.answer(message, self.strings("api_error"))
                        return
                    
                    # API returns text/html content-type for json, so we ignore it
                    data = await response.json(content_type=None)

            quote_text = data.get("quoteText", "").strip()
            quote_author = data.get("quoteAuthor", "").strip() or self.strings("unknown_author")

            result = f"<blockquote>{quote_text}</blockquote>\n\n<b>— {quote_author}</b>"
            await utils.answer(message, result)

        except Exception as e:
            await utils.answer(message, f"<b>🚫 Произошла ошибка:</b>\n<code>{e}</code>")