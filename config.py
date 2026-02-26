import os

"""
Глобальная конфигурация бота.

Все значения можно переопределить через переменные окружения.
"""

# Токен Telegram‑бота
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "8384870189:AAEViu4Ee_0jD6-SU7F6TQMHIJCLUyT-SI4")

# Пути к базам данных
USERS_DB_PATH: str = os.getenv("USERS_DB_PATH", "users_database.sqlite")
BAD_SCORE_DB_PATH: str = os.getenv("BAD_SCORE_DB_PATH", "bad_score.sqlite")
STICKER_DB_PATH: str = os.getenv("STICKER_DB_PATH", "sticker_counter.sqlite")
MEME_CACHE_DB_PATH: str = os.getenv("MEME_CACHE_DB_PATH", "meme_cache.sqlite")

# Вероятности ответов бота
REPLY_PROB_BAD_WORDS: float = 0.20
REPLY_PROB_NO: float = 0.40
REPLY_PROB_NO_UKR: float = 0.40
REPLY_PROB_YES: float = 0.50
REPLY_PROB_AGA: float = 0.90
REPLY_PROB_STICKER_ANNOUNCE: float = 0.30

