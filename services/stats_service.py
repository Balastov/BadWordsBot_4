import logging
from typing import List, Sequence, Tuple

from bot_app import sticker_counter
from BadScore_1 import get_bad_score, get_top_bad_scores, increase_bad_score


logger = logging.getLogger(__name__)


# Тип записи о пользователе: username, first_name, last_name, score
UserScoreRow = Tuple[str, str, str, int]


def increment_bad_score(
    user_id: int,
    username: str,
    first_name: str,
    last_name: str,
    chat_id: int,
) -> int | None:
    """Увеличивает счётчик матов пользователя и возвращает новое значение."""
    return increase_bad_score(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        chat_id=chat_id,
    )


def get_bad_top(chat_id: int, limit: int = 10) -> Sequence[UserScoreRow]:
    """Возвращает топ матершинников для чата."""
    return get_top_bad_scores(chat_id, limit=limit)


def get_user_bad_score(user_id: int, chat_id: int) -> int:
    """Возвращает текущий счёт матов пользователя."""
    return get_bad_score(user_id, chat_id)


def get_user_sticker_stats(user_id: int, chat_id: int) -> dict:
    """Возвращает статистику стикеров пользователя."""
    return sticker_counter.get_sticker_stats(user_id, chat_id)


def get_sticker_top(chat_id: int, limit: int = 10):
    """Возвращает топ пользователей по количеству стикеров и общее число стикеров."""
    top_users = sticker_counter.get_top_sticker_users(chat_id, limit=limit)
    total_stickers = sticker_counter.get_total_stickers_in_chat(chat_id)
    return top_users, total_stickers


__all__ = [
    "increment_bad_score",
    "get_bad_top",
    "get_user_bad_score",
    "get_user_sticker_stats",
    "get_sticker_top",
]

