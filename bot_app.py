import logging

import telebot

from config import TELEGRAM_BOT_TOKEN
from DailyEvents import DailyEvents
from StickerCounter import StickerCounter
from MemeSender import MemeSender


logger = logging.getLogger(__name__)


if not TELEGRAM_BOT_TOKEN:
    logger.warning(
        "TELEGRAM_BOT_TOKEN не задан. Установите переменную окружения TELEGRAM_BOT_TOKEN."
    )


# Единый экземпляр бота для всех модулей
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN or "MISSING_TOKEN")

# Сервисы, завязанные на боте
daily_events = DailyEvents(bot)
sticker_counter = StickerCounter()
meme_sender = MemeSender(bot)

