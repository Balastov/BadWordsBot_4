import logging
import random
import string
from typing import Iterable

from bot_app import bot
from config import (
    REPLY_PROB_AGA,
    REPLY_PROB_BAD_WORDS,
    REPLY_PROB_NO,
    REPLY_PROB_NO_UKR,
    REPLY_PROB_YES,
)
from constants import bad_words, exeptions


logger = logging.getLogger(__name__)

# Предподготовленные множества для быстрых проверок
BAD_WORDS_SET = set(word.lower() for word in bad_words)
EXCEPTIONS_SET = set(word.lower() for word in exeptions)


def _sanitize_text(text: str) -> str:
    """
    Удаляет знаки препинания и приводит текст к нижнему регистру.
    """
    translator = str.maketrans({ch: " " for ch in string.punctuation})
    return text.translate(translator).lower()


def contains_bad_words(text: str) -> bool:
    """
    Проверяет, содержит ли текст матерные слова.

    Логика:
    - приводим текст к нижнему регистру;
    - удаляем из текста все вхождения исключений;
    - проверяем, есть ли в оставшемся тексте слова из списка матов.
    """
    if not text or not isinstance(text, str):
        return False

    text_lower = text.lower()

    # Удаляем все исключения из текста, чтобы они не мешали поиску матов
    sanitized = text_lower
    for ex in exeptions:
        if ex:
            sanitized = sanitized.replace(ex.lower(), " ")

    # Смотрим, остался ли в тексте хоть один мат
    return any(bad_word in sanitized for bad_word in BAD_WORDS_SET)


def should_bot_reply(probability: float = REPLY_PROB_BAD_WORDS, debug: bool = False) -> bool:
    """
    Определяет, должен ли бот ответить с заданной вероятностью.
    """
    chance = random.random()
    should_reply = chance <= probability

    if debug:
        status = "✅ ОТВЕТ" if should_reply else "🔇 МОЛЧАНИЕ"
        logger.info(
            "🎲 Вероятность ответа: %.2f <= %.2f -> %s",
            chance,
            probability,
            status,
        )

    return should_reply


def bot_reply_with_probability(
    message,
    response_text: str,
    probability: float,
    debug: bool = True,
) -> bool:
    """
    Отправляет ответ с заданной вероятностью.

    Возвращает True, если ответ был отправлен.
    """
    if should_bot_reply(probability, debug):
        bot.reply_to(message, response_text)
        if debug:
            logger.info(
                "🗣️ Бот ответил (шанс %.0f%%): %s",
                probability * 100,
                (response_text or "")[:50],
            )
        return True

    if debug:
        logger.info("🔇 Бот промолчал (шанс %.0f%%)", probability * 100)
    return False


__all__ = [
    "contains_bad_words",
    "should_bot_reply",
    "bot_reply_with_probability",
    "REPLY_PROB_BAD_WORDS",
    "REPLY_PROB_NO",
    "REPLY_PROB_NO_UKR",
    "REPLY_PROB_YES",
    "REPLY_PROB_AGA",
]

