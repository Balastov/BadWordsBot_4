import logging
import sqlite3
from typing import List, Optional, Sequence, Tuple

from config import USERS_DB_PATH


logger = logging.getLogger(__name__)


def init_users_db(db_path: str = USERS_DB_PATH) -> None:
    """Создаёт таблицу chat_users при необходимости."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_users (
                    user_id INTEGER,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    chat_id INTEGER,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, chat_id)
                )
                """
            )
        logger.info("✅ База данных пользователей создана/инициализирована")
    except Exception as e:
        logger.error("❌ Ошибка при создании базы пользователей: %s", e)


def add_user_to_db(
    user_id: int,
    username: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
    chat_id: int,
    db_path: str = USERS_DB_PATH,
) -> bool:
    """Добавляет пользователя в БД, если он ещё не существует."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 1 FROM chat_users
                WHERE user_id = ? AND chat_id = ?
                """,
                (user_id, chat_id),
            )
            existing_user = cursor.fetchone()

            if existing_user:
                logger.info(
                    "ℹ️ Пользователь %s уже существует в базе",
                    username or first_name,
                )
                return False

            cursor.execute(
                """
                INSERT INTO chat_users
                (user_id, username, first_name, last_name, chat_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, username, first_name, last_name, chat_id),
            )

        logger.info("✅ Пользователь %s добавлен в базу", username or first_name)
        return True
    except Exception as e:
        logger.error("❌ Ошибка при добавлении пользователя: %s", e)
        return False


def get_chat_users(
    chat_id: int, db_path: str = USERS_DB_PATH
) -> Sequence[Tuple[int, Optional[str], Optional[str], Optional[str], int]]:
    """Возвращает всех пользователей указанного чата."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT user_id, username, first_name, last_name, chat_id
                FROM chat_users
                WHERE chat_id = ?
                ORDER BY first_name
                """,
                (chat_id,),
            )
            users = cursor.fetchall()
        return users
    except Exception as e:
        logger.error("❌ Ошибка при получении пользователей: %s", e)
        return []


def is_user_in_db(user_id: int, chat_id: int, db_path: str = USERS_DB_PATH) -> bool:
    """Проверяет, есть ли пользователь в БД."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 1 FROM chat_users
                WHERE user_id = ? AND chat_id = ?
                """,
                (user_id, chat_id),
            )
            result = cursor.fetchone()
        return result is not None
    except Exception as e:
        logger.error("❌ Ошибка при проверке пользователя: %s", e)
        return False


def auto_collect_users_from_message(message) -> None:
    """
    Извлекает пользователя из сообщения и при необходимости добавляет в БД.
    Ожидает объект telebot.types.Message.
    """
    user = message.from_user
    if user is None or user.is_bot:
        return

    if not is_user_in_db(user.id, message.chat.id):
        added = add_user_to_db(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            chat_id=message.chat.id,
        )
        if added:
            logger.info(
                "✅ Добавлен новый пользователь: %s",
                user.username or user.first_name,
            )
    else:
        logger.info(
            "ℹ️ Пользователь уже в базе: %s",
            user.username or user.first_name,
        )

