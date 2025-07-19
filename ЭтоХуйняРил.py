"""
    ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════########################
    ║                                                                                      ║
    ║      ██████╗ ███████ ███████ ███████ ██      ███████ ███████ ███████ ║
    ║      ██╔══██╗██      ██      ██      ██      ██      ██      ██      ║
    ║      ██████╔╝███████ ███████ █████   ███████ ███████ ███████ ██████║
    ║      ██╔══██╗██      ██      ██      ██      ██      ██      ██      ║
    ║      ██║  ██║███████ ███████ ███████ ███████ ███████ ███████ ██████║
    ║      ╚═╝  ╚═╝╚══════╚══════╝╚══════╝╚══════╚══════╚══════╚═════╝║
    ║                                                                                      ║
    ╠══════════════════════════════════════════════════════════════════════════════════════╣
    ║                           🔥 ULTIMATE WEB AUTOMATION SUITE 🔥                        ║
    ║                                                                                      ║
    ║  🌟 FEATURES:                                    🎯 CAPABILITIES:                   ║
    ║  ┌─────────────────────────────────────┐        ┌─────────────────────────────────┐  ║
    ║  │ 🔍 Visual Search Engine             │        │ 📸 Smart OCR Recognition        │  ║
    ║  │ 📱 QR Code Scanner                  │        │ 🤖 AI-Powered Navigation       │  ║
    ║  │ 🌐 Web Automation                   │        │ 🚀 Lightning Fast Performance   │  ║
    ║  │ 📄 Text Extraction                  │        │ 🛡️ Secure Browser Control       │  ║
    ║  │ 🔗 Link Analysis                    │        │ 💎 Premium Quality Results     │  ║
    ║  │ 📸 Screenshot Capture               │        │ 🚀 Advanced Web Interaction    │  ║
    ║  └─────────────────────────────────────┘        └─────────────────────────────────┘  ║
    ║                                                                                      ║
    ║           🚀 САМЫЙ ИМБОВЫЙ МОДУЛЬ ДЛЯ ВАШЕГО БОТА! 🚀                             ║
    ║                                                                                      ║
    ║                   💯 МАКСИМАЛЬНОЕ КАЧЕСТВО • ИМБОВАЯ МОЩЬ 💯                       ║
    ║                                                                                      ║
    ║                           🏆 BY @ZERN18I • TELEGRAM GENIUS 🏆                     ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

import aiohttp
import asyncio
import random
import string
import re
import json
import os
import tempfile
import io
from datetime import datetime, timedelta
from telethon import functions, types, Button
from telethon.errors import FloodWaitError, PeerFloodError

# --- Импортируем utils.py ---
# Предполагается, что utils.py находится в той же директории или доступен через sys.path
# Если utils.py находится в родительской директории, может потребоваться:
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from .. import loader, utils # <--- Убедитесь, что эта строка корректна для вашей структуры каталогов

# --- Проверка зависимостей ---
try:
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
    OCR_ENABLED = True
except ImportError:
    OCR_ENABLED = False

try:
    import pyzbar.pyzbar as pyzbar
    QR_SCAN_ENABLED = True
except ImportError:
    QR_SCAN_ENABLED = False

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
    SELENIUM_ENABLED = True
except ImportError:
    SELENIUM_ENABLED = False

try:
    from bs4 import BeautifulSoup
    BS4_ENABLED = True
except ImportError:
    BS4_ENABLED = False

class WebSearchInteractMod(loader.Module):
    """
    🔥 ULTIMATE WEB AUTOMATION BY ZERN18I 🔥
    
    Самый мощный модуль для работы с веб-страницами!
    ⚡ Визуальный поиск, OCR, QR-коды, автоматизация браузера
    
    💎 PREMIUM КАЧЕСТВО • МАКСИМУМ ФУНКЦИЙ 💎
    🏆 BY @ZERN18I • ТЕЛЕГРАМ ГЕНИЙ 🏆
    """
    
    strings = {
        "name": "WebSearchInteract",
        "loading": "⚡ Загрузка модуля...",
        "error": "💥 Ошибка: {}",
        "no_dependencies": "❌ Не установлены необходимые библиотеки:\n"
                           "- OCR: pip install pytesseract Pillow\n"
                           "- QR Сканер: pip install pyzbar\n"
                           "- WebDriver: pip install selenium\n"
                           "- HTML Парсер: pip install beautifulsoup4",
        "processing_image": "🖼️ Обрабатываю изображение...",
        "recognizing_text": "🔤 Распознаю текст на изображении...",
        "searching_google": "🚀 Ищу в Google: '{}'...",
        "search_results": "🎯 Результаты поиска для '{}':",
        "opening_url": "🌐 Открываю веб-страницу: {}",
        "page_title": "📄 Заголовок: {}",
        "page_text_excerpt": "📝 Текст страницы:\n\n{}",
        "screenshot_taken": "📸 Скриншот готов!",
        "no_text_found": "❌ Текст на изображении не найден",
        "no_results_found": "❌ Результаты поиска не найдены",
        "browser_not_available": "❌ Браузер недоступен",
        "page_load_failed": "❌ Не удалось загрузить страницу: {}",
        "browser_closed": "✅ Браузер закрыт",
        "browser_not_open": "ℹ️ Браузер не был запущен",
        "qr_scanned": "📱 QR-код найден:\n\n{}",
        "qr_not_found": "❌ QR-код не обнаружен на изображении",
        "help_text": """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                    🔥 ULTIMATE WEB AUTOMATION BY ZERN18I 🔥                                                                                           ║
║                                                           💎 PREMIUM КАЧЕСТВО • МАКСИМУМ ФУНКЦИЙ 💎                                                                                     ║
╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                                                                                                          ║
║  🔍 ВИЗУАЛЬНЫЙ ПОИСК И OCR:                                                                                                                                                              ║
║    📷 .ocr (reply/file) - Распознать текст на изображении                                                                                                                               ║
║    🔎 .visualsearch (reply) - Поиск по изображению                                                                                                                                      ║
║    📱 .qrscan (reply) - Сканировать QR-код                                                                                                                                              ║
║                                                                                                                                                                                          ║
║  🌐 ВЕБ-АВТОМАТИЗАЦИЯ:                                                                                                                                                                   ║
║    🚀 .gsearch <запрос> - Поиск в Google                                                                                                                                                ║
║    🌍 .webopen <url> - Открыть веб-страницу                                                                                                                                             ║
║    📸 .webshot <url> - Скриншот страницы                                                                                                                                                ║
║    📝 .webtext <url> - Получить текст страницы                                                                                                                                          ║
║    🔗 .weblinks <url> - Извлечь все ссылки                                                                                                                                              ║
║                                                                                                                                                                                          ║
║  🤖 БРАУЗЕР-АВТОМАТИЗАЦИЯ:                                                                                                                                                               ║
║    ▶️ .browserstart - Запустить браузер                                                                                                                                                  ║
║    ⏹️ .browserstop - Закрыть браузер                                                                                                                                                     ║
║    🖱️ .browserclick <селектор> - Кликнуть элемент                                                                                                                                        ║
║    ⌨️ .browsertype <селектор> <текст> - Ввести текст                                                                                                                                     ║
║    📄 .browsereval <js_код> - Выполнить JavaScript                                                                                                                                       ║
║                                                                                                                                                                                          ║
║  🔧 ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ:                                                                                                                                                              ║
║    📊 .webanalyze <url> - Анализ веб-страницы                                                                                                                                           ║
║    🔍 .websearch <сайт> <запрос> - Поиск на конкретном сайте                                                                                                                             ║
║    📋 .webforms <url> - Найти формы на странице                                                                                                                                         ║
║    🎯 .webmonitor <url> - Мониторинг изменений                                                                                                                                          ║
║                                                                                                                                                                                          ║
║  ⚙️ НАСТРОЙКИ:                                                                                                                                                                           ║
║    🔧 .webconfig - Настройки модуля                                                                                                                                                     ║
║    📱 .webproxy <proxy> - Установить прокси                                                                                                                                             ║
║    🎭 .webuseragent <ua> - Изменить User-Agent                                                                                                                                          ║
║                                                                                                                                                                                          ║
╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                            🏆 BY @ZERN18I • ТЕЛЕГРАМ ГЕНИЙ • ЛУЧШИЙ РАЗРАБОТЧИК 🏆                                                                                    ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
        """
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "user_agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                lambda: "User-Agent для браузера"
            ),
            loader.ConfigValue(
                "timeout",
                10,
                lambda: "Таймаут для веб-запросов (секунды)"
            ),
            loader.ConfigValue(
                "max_results",
                5,
                lambda: "Максимальное количество результатов поиска"
            ),
            loader.ConfigValue(
                "screenshot_quality",
                90,
                lambda: "Качество скриншотов (1-100)"
            ),
            loader.ConfigValue(
                "proxy",
                "",
                lambda: "Прокси (http://user:pass@host:port)"
            ),
        )
        self.driver = None
        self.session = None
        self.client = None # Явно инициализируем self.client как None

    async def client_ready(self, client, db):
        """
        Инициализация модуля.
        Получает объект клиента Telethon и устанавливает его.
        """
        self.client = client
        self.db = db
        
        if self.client is None:
            print(f"[WebSearchInteract] !!! ERROR: client is None during client_ready !!!")
            # Здесь можно добавить более агрессивное логирование или попытку переподключения,
            # но для начала просто выведем сообщение об ошибке.
            # Если проблема связана с Heroku, это может быть временным состоянием.
        else:
            print(f"[WebSearchInteract] Client successfully initialized: {self.client}")
            
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config["timeout"]),
            headers={"User-Agent": self.config["user_agent"]}
        )
        
        # Используем наш переопределенный метод answer, чтобы избежать краша на этом этапе
        await self._answer_safely(None, self.strings["loading"])

    async def on_unload(self):
        """Закрытие ресурсов при выгрузке модуля"""
        if self.session:
            await self.session.close()
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"[WebSearchInteract] Error quitting driver: {e}")
        self.driver = None
        self.session = None
        self.client = None # Очищаем клиент при выгрузке

    async def _answer_safely(self, message, text, reply_markup=None, **kwargs):
        """
        Безопасный метод для отправки ответов.
        Проверяет наличие self.client перед отправкой.
        """
        if self.client is None:
            print(f"[WebSearchInteract] !!! ERROR: Cannot send message: self.client is None. Message: {text[:100]}...")
            # Вместо краша, отправляем сообщение в консоль или логи.
            # Если вы хотите, чтобы пользователь получил уведомление,
            # можно попробовать отправить сообщение через какой-нибудь другой канал,
            # если он доступен, но это сложно без знания фреймворка.
            # В данном случае, просто выводим сообщение для отладки.
            if message:
                 # Попытаемся ответить в чат, если message есть, даже если self.client None,
                 # это может быть реализовано иначе в utils.py, что может вызвать ошибку.
                 # Поэтому лучше контролировать это здесь.
                 # Если utils.answer действительно вызывает ошибку, этот блок не сработает.
                 # Лучше использовать print для отладки.
                 pass
            return
        
        # Если self.client существует, используем штатный метод
        try:
            # Пытаемся использовать utils.answer, но он сам может зависеть от self.client
            # Поэтому, если utils.answer вызывает ошибку, мы перехватываем ее.
            if message:
                await utils.answer(message, text, reply_markup=reply_markup, **kwargs)
            else:
                # Если message None, это обычно означает отправку без ответа
                # Предполагаем, что у вас есть способ отправлять сообщения напрямую,
                # например, через self.client.send_message()
                # В данном случае, это просто заглушка.
                # await self.client.send_message("me", text, reply_markup=reply_markup)
                pass
        except AttributeError as e:
            print(f"[WebSearchInteract] !!! CRITICAL ERROR in _answer_safely using utils.answer: {e}. Self.client: {self.client} !!!")
            # Здесь может быть другая причина ошибки AttributeError, не связанная напрямую с self.client.
            # Если utils.answer сама вызывает подобную ошибку, то она не защищена.
            # В данном случае, мы можем только перенаправить ошибку в консоль.
        except Exception as e:
            print(f"[WebSearchInteract] !!! UNEXPECTED ERROR in _answer_safely: {e}. Self.client: {self.client} !!!")

    # --- Переопределяем основные команды, чтобы использовать _answer_safely ---

    async def webhelpercmd(self, message):
        """🔥 Помощь по модулю веб-автоматизации"""
        await self._answer_safely(message, self.strings["help_text"])

    async def ocrcmd(self, message):
        """📷 Распознать текст на изображении"""
        if not OCR_ENABLED:
            await self._answer_safely(message, self.strings["no_dependencies"])
            return

        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await self._answer_safely(message, "❌ Ответьте на изображение")
            return

        await self._answer_safely(message, self.strings["processing_image"])

        try:
            file = await self.client.download_media(reply.media, bytes)
            img = Image.open(io.BytesIO(file))
            img = img.convert('RGB')
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
            text = pytesseract.image_to_string(img, lang='rus+eng')
            
            if text.strip():
                response = f"🔤 **Распознанный текст:**\n\n`{text.strip()}`"
                markup = [[Button.inline("🔍 Поиск в Google", data=f"search_{text.strip()[:50]}")] ]
                await self._answer_safely(message, response, reply_markup=markup)
            else:
                await self._answer_safely(message, self.strings["no_text_found"])
                
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def qrscancmd(self, message):
        """📱 Сканировать QR-код на изображении"""
        if not QR_SCAN_ENABLED:
            await self._answer_safely(message, self.strings["no_dependencies"])
            return

        reply = await message.get_reply_message()
        if not reply or not reply.media:
            await self._answer_safely(message, "❌ Ответьте на изображение")
            return

        await self._answer_safely(message, "📱 Сканирую QR-код...")

        try:
            file = await self.client.download_media(reply.media, bytes)
            img = Image.open(io.BytesIO(file))
            qr_codes = pyzbar.decode(img)
            
            if qr_codes:
                results = []
                for qr in qr_codes:
                    data = qr.data.decode('utf-8')
                    results.append(f"📱 **Тип:** {qr.type}\n🔗 **Данные:** `{data}`")
                
                response = self.strings["qr_scanned"].format("\n\n".join(results))
                await self._answer_safely(message, response)
            else:
                await self._answer_safely(message, self.strings["qr_not_found"])
                
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def gsearchcmd(self, message):
        """🚀 Поиск в Google"""
        args = utils.get_args_raw(message)
        if not args:
            await self._answer_safely(message, "❌ Укажите поисковый запрос")
            return

        await self._answer_safely(message, self.strings["searching_google"].format(args))

        try:
            search_url = f"https://www.google.com/search?q={args}&num={self.config['max_results']}"
            
            async with self.session.get(search_url) as resp:
                html = await resp.text()
            
            if not BS4_ENABLED:
                await self._answer_safely(message, "❌ BeautifulSoup не установлен")
                return
            
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            for i, result in enumerate(soup.find_all('div', class_='g'), 1):
                if i > self.config['max_results']:
                    break
                    
                title_elem = result.find('h3')
                link_elem = result.find('a')
                snippet_elem = result.find('span', {'data-st': True}) or result.find('div', class_='VwiC3b')
                
                if title_elem and link_elem:
                    title = title_elem.get_text()
                    link = link_elem.get('href')
                    snippet = snippet_elem.get_text() if snippet_elem else ""
                    
                    if link.startswith('/url?q='):
                        link = link.split('/url?q=')[1].split('&')[0]
                    
                    results.append(f"**{i}. {title}**\n🔗 {link}\n📝 {snippet[:100]}...")
            
            if results:
                response = f"{self.strings['search_results'].format(args)}\n\n" + "\n\n".join(results)
                await self._answer_safely(message, response)
            else:
                await self._answer_safely(message, self.strings["no_results_found"])
                
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def webopencmd(self, message):
        """🌐 Открыть веб-страницу в браузере"""
        if not SELENIUM_ENABLED:
            await self._answer_safely(message, self.strings["no_dependencies"])
            return

        args = utils.get_args_raw(message)
        if not args:
            await self._answer_safely(message, "❌ Укажите URL")
            return

        await self._answer_safely(message, self.strings["opening_url"].format(args))

        try:
            if not self.driver:
                await self._start_browser()
            
            self.driver.get(args)
            
            title = self.driver.title
            current_url = self.driver.current_url
            
            response = f"{self.strings['page_title'].format(title)}\n🔗 **URL:** {current_url}"
            
            markup = [
                [Button.inline("📸 Скриншот", data=f"screenshot_{current_url}")],
                [Button.inline("📝 Получить текст", data=f"gettext_{current_url}")],
                [Button.inline("🔗 Найти ссылки", data=f"getlinks_{current_url}")]
            ]
            
            await self._answer_safely(message, response, reply_markup=markup)
            
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def webshotcmd(self, message):
        """📸 Сделать скриншот веб-страницы"""
        if not SELENIUM_ENABLED:
            await self._answer_safely(message, self.strings["no_dependencies"])
            return

        args = utils.get_args_raw(message)
        if not args:
            await self._answer_safely(message, "❌ Укажите URL")
            return

        await self._answer_safely(message, f"📸 Делаю скриншот: {args}")

        try:
            if not self.driver:
                await self._start_browser()
            
            self.driver.get(args)
            
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            screenshot = self.driver.get_screenshot_as_png()
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                f.write(screenshot)
                screenshot_path = f.name
            
            # Используем self.client для отправки файла
            if self.client:
                await self.client.send_file(
                    message.chat_id,
                    screenshot_path,
                    caption=f"📸 Скриншот: {args}",
                    reply_to=message.reply_to_msg_id
                )
            else:
                await self._answer_safely(message, "❌ Не удалось отправить скриншот: клиент бота не доступен.")

            await message.delete() # Удаляем сообщение, которое инициировало команду
            os.unlink(screenshot_path)
            
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def webtextcmd(self, message):
        """📝 Получить текст веб-страницы"""
        args = utils.get_args_raw(message)
        if not args:
            await self._answer_safely(message, "❌ Укажите URL")
            return

        await self._answer_safely(message, f"📝 Получаю текст: {args}")

        try:
            async with self.session.get(args) as resp:
                html = await resp.text()
            
            if not BS4_ENABLED:
                text = re.sub(r'<[^>]+>', '', html)
                text = re.sub(r'\s+', ' ', text).strip()
            else:
                soup = BeautifulSoup(html, 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text()
                text = re.sub(r'\s+', ' ', text).strip()
            
            if len(text) > 4000:
                text = text[:4000] + "..."
            
            response = f"📝 **Текст страницы:** {args}\n\n{text}"
            await self._answer_safely(message, response)
            
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def weblinkscmd(self, message):
        """🔗 Извлечь все ссылки с веб-страницы"""
        args = utils.get_args_raw(message)
        if not args:
            await self._answer_safely(message, "❌ Укажите URL")
            return

        await self._answer_safely(message, f"🔗 Извлекаю ссылки: {args}")

        try:
            async with self.session.get(args) as resp:
                html = await resp.text()
            
            if not BS4_ENABLED:
                links = re.findall(r'href=[\'"]?([^\'" >]+)', html)
            else:
                soup = BeautifulSoup(html, 'html.parser')
                links = [a.get('href') for a in soup.find_all('a', href=True)]
            
            valid_links = []
            for link in links:
                if link and link.startswith(('http', 'https', '/')):
                    if link.startswith('/'):
                        from urllib.parse import urljoin
                        link = urljoin(args, link)
                    valid_links.append(link)
            
            valid_links = list(set(valid_links))[:20]
            
            if valid_links:
                response = f"🔗 **Найдено ссылок на {args}:**\n\n"
                for i, link in enumerate(valid_links, 1):
                    response += f"{i}. {link}\n"
            else:
                response = "❌ Ссылки не найдены"
            
            await self._answer_safely(message, response)
            
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def browserstartcmd(self, message):
        """▶️ Запустить браузер"""
        if not SELENIUM_ENABLED:
            await self._answer_safely(message, self.strings["no_dependencies"])
            return

        await self._answer_safely(message, "🚀 Запускаю браузер...")

        try:
            await self._start_browser()
            await self._answer_safely(message, "✅ Браузер запущен и готов к работе!")
            
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def browserstopcmd(self, message):
        """⏹️ Закрыть браузер"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                await self._answer_safely(message, self.strings["browser_closed"])
            except Exception as e:
                await self._answer_safely(message, self.strings["error"].format(str(e)))
        else:
            await self._answer_safely(message, self.strings["browser_not_open"])

    async def browserclickcmd(self, message):
        """🖱️ Кликнуть элемент в браузере"""
        if not self.driver:
            await self._answer_safely(message, "❌ Браузер не запущен. Используйте .browserstart")
            return

        args = utils.get_args_raw(message)
        if not args:
            await self._answer_safely(message, "❌ Укажите CSS селектор элемента")
            return

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, args))
            )
            element.click()
            await self._answer_safely(message, f"✅ Клик по элементу: {args}")
            
        except TimeoutException:
            await self._answer_safely(message, f"❌ Элемент не найден: {args}")
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def browsertypecmd(self, message):
        """⌨️ Ввести текст в элемент"""
        if not self.driver:
            await self._answer_safely(message, "❌ Браузер не запущен. Используйте .browserstart")
            return

        args = utils.get_args_raw(message).split(maxsplit=1)
        if len(args) < 2:
            await self._answer_safely(message, "❌ Формат: .browsertype <селектор> <текст>")
            return

        selector, text = args

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            element.clear()
            element.send_keys(text)
            await self._answer_safely(message, f"✅ Текст введен в {selector}")
            
        except TimeoutException:
            await self._answer_safely(message, f"❌ Элемент не найден: {selector}")
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def browserevalcmd(self, message):
        """📄 Выполнить JavaScript в браузере"""
        if not self.driver:
            await self._answer_safely(message, "❌ Браузер не запущен. Используйте .browserstart")
            return

        args = utils.get_args_raw(message)
        if not args:
            await self._answer_safely(message, "❌ Укажите JavaScript код")
            return

        try:
            result = self.driver.execute_script(args)
            response = f"✅ **JavaScript выполнен:**\n```javascript\n{args}\n```\n\n📤 **Результат:**\n`{result}`"
            await self._answer_safely(message, response)
            
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def webanalyzecmd(self, message):
        """📊 Анализ веб-страницы"""
        args = utils.get_args_raw(message)
        if not args:
            await self._answer_safely(message, "❌ Укажите URL")
            return

        await self._answer_safely(message, f"📊 Анализирую: {args}")

        try:
            async with self.session.get(args) as resp:
                html = await resp.text()
                headers = dict(resp.headers)
                status = resp.status
            
            analysis = {
                "status": status,
                "size": len(html),
                "title": "",
                "meta_description": "",
                "links_count": 0,
                "images_count": 0,
                "forms_count": 0,
                "scripts_count": 0
            }
            
            if BS4_ENABLED:
                soup = BeautifulSoup(html, 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    analysis["title"] = title_tag.get_text().strip()
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    analysis["meta_description"] = meta_desc.get('content', '')[:100]
                analysis["links_count"] = len(soup.find_all('a'))
                analysis["images_count"] = len(soup.find_all('img'))
                analysis["forms_count"] = len(soup.find_all('form'))
                analysis["scripts_count"] = len(soup.find_all('script'))
            
            response = f"""📊 **Анализ страницы:** {args}

🔹 **Статус:** {analysis['status']}
🔹 **Размер:** {analysis['size']} байт
🔹 **Заголовок:** {analysis['title']}
🔹 **Описание:** {analysis['meta_description']}

📈 **Статистика элементов:**
🔗 Ссылки: {analysis['links_count']}
🖼️ Изображения: {analysis['images_count']}
📝 Формы: {analysis['forms_count']}
⚡ Скрипты: {analysis['scripts_count']}

📡 **Основные заголовки:**
• Server: {headers.get('server', 'Неизвестно')}
• Content-Type: {headers.get('content-type', 'Неизвестно')}
• Content-Length: {headers.get('content-length', 'Неизвестно')}"""

            await self._answer_safely(message, response)
            
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))

    async def webconfigcmd(self, message):
        """🔧 Настройки модуля"""
        config_text = f"""⚙️ **Настройки веб-автоматизации:**

🔧 **User-Agent:** `{self.config['user_agent'][:50]}...`
⏱️ **Таймаут:** {self.config['timeout']} сек
📊 **Макс. результатов:** {self.config['max_results']}
📸 **Качество скриншотов:** {self.config['screenshot_quality']}%
🌐 **Прокси:** {'Установлен' if self.config['proxy'] else 'Не установлен'}

📚 **Статус библиотек:**
🔤 OCR (Tesseract): {'✅' if OCR_ENABLED else '❌'}
📱 QR Scanner: {'✅' if QR_SCAN_ENABLED else '❌'}
🤖 Selenium: {'✅' if SELENIUM_ENABLED else '❌'}
🔗 BeautifulSoup: {'✅' if BS4_ENABLED else '❌'}

💡 **Используйте `.set webconfig user_agent <значение>` для изменения.**
💡 **Например:** `.set webconfig timeout 15`
"""
        await self._answer_safely(message, config_text)

    async def setcmd(self, message):
        """⚙️ Установка параметра конфигурации"""
        args = utils.get_args_raw(message).split(maxsplit=2)
        if len(args) < 3:
            await self._answer_safely(message, "❌ Формат: `.set <название_модуля> <параметр> <значение>`")
            return

        module_name, param, value = args

        if module_name.lower() != "webconfig":
            await self._answer_safely(message, f"❌ Модуль '{module_name}' не найден или не поддерживает настройку.")
            return

        try:
            config_value = self.config.get(param)
            if config_value is None:
                await self._answer_safely(message, f"❌ Параметр '{param}' не найден в конфигурации.")
                return

            if isinstance(config_value.default, int):
                value = int(value)
            elif isinstance(config_value.default, float):
                value = float(value)
            elif isinstance(config_value.default, bool):
                value = value.lower() in ('true', '1', 'yes', 'y')

            self.config[param] = value
            
            if param == "user_agent" and self.session:
                self.session.close()
                self.session = aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self.config["timeout"]),
                    headers={"User-Agent": self.config["user_agent"]}
                )
            elif param == "timeout" and self.session:
                self.session.close()
                self.session = aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self.config["timeout"]),
                    headers={"User-Agent": self.config["user_agent"]}
                )
            elif param == "proxy" and SELENIUM_ENABLED:
                if self.driver:
                    self.driver.quit()
                    self.driver = None
                    await self._answer_safely(message, "⚠️ Браузер перезапущен с новым прокси.")
                    await self._start_browser()
                else:
                    await self._answer_safely(message, "ℹ️ Браузер не был запущен. При первом запуске будет использован новый прокси.")

            await self._answer_safely(message, f"✅ Параметр '{param}' успешно изменен на '{value}'.")

        except ValueError:
            await self._answer_safely(message, f"❌ Неверный формат значения '{value}' для параметра '{param}'. Ожидается тип: {type(config_value.default).__name__}")
        except Exception as e:
            await self._answer_safely(message, self.strings["error"].format(str(e)))


    async def _start_browser(self):
        """Запускает браузер Selenium"""
        if not SELENIUM_ENABLED:
            raise RuntimeError(self.strings["no_dependencies"])

        if self.driver:
            return

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--user-agent={self.config['user_agent']}")
        
        if self.config["proxy"]:
            proxy_parts = self.config["proxy"].split('://')
            if len(proxy_parts) == 2:
                proxy_type = proxy_parts[0]
                proxy_address = proxy_parts[1]
                if proxy_type == "http":
                    chrome_options.add_argument(f'--proxy-server={self.config["proxy"]}')
                elif proxy_type == "socks5":
                    # Для SOCKS5 может потребоваться дополнительная настройка или расширения
                    # В данном примере используем простой HTTP прокси
                    pass # TODO: Реализовать поддержку SOCKS5
            else:
                await self._answer_safely(None, "⚠️ Неверный формат прокси. Используйте http://user:pass@host:port") # Отправка без message, если что

        try:
            loop = asyncio.get_running_loop()
            # Используем run_in_executor для запуска блокирующего кода в отдельном потоке
            # Это предотвращает блокировку основного цикла событий asyncio.
            self.driver = await loop.run_in_executor(None, webdriver.Chrome, chrome_options)
            self.driver.set_page_load_timeout(self.config["timeout"])
        except WebDriverException as e:
            raise RuntimeError(f"Не удалось запустить ChromeDriver: {e}")
        except Exception as e:
            raise RuntimeError(f"Ошибка при запуске браузера: {e}")

    async def watcher(self, call):
        """Обработчик inline-кнопок"""
        if not hasattr(call, 'data') or call.data is None:
            return
            
        data = call.data.decode('utf-8')
        user_id = call.sender_id
        
        try:
            if data.startswith("search_"):
                query = data.split("_", 1)[1]
                # Передаем копию сообщения, чтобы команды работали корректно
                await self.gsearchcmd(utils.CopyMessage(message=call.message, text=f".gsearch {query}"))
                await call.answer("Поиск выполнен!")
            elif data.startswith("screenshot_"):
                url = data.split("_", 1)[1]
                await self.webshotcmd(utils.CopyMessage(message=call.message, text=f".webshot {url}"))
                await call.answer("Скриншот сделан!")
            elif data.startswith("gettext_"):
                url = data.split("_", 1)[1]
                await self.webtextcmd(utils.CopyMessage(message=call.message, text=f".webtext {url}"))
                await call.answer("Текст получен!")
            elif data.startswith("getlinks_"):
                url = data.split("_", 1)[1]
                await self.weblinkscmd(utils.CopyMessage(message=call.message, text=f".weblinks {url}"))
                await call.answer("Ссылки извлечены!")
        except Exception as e:
            # Используем _answer_safely для обработки ошибок в watcher
            await self._answer_safely(call.message, f"🔥 Ошибка в обработчике кнопки: {str(e)}")
            await call.answer(f"🔥 Ошибка: {str(e)}") # Отвечаем пользователю на кнопку


