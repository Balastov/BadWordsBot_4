import logging
import threading
import time
from typing import Dict

from bot_app import bot


logger = logging.getLogger(__name__)

# chat_id -> message_id активного меню
active_menus: Dict[int, int] = {}


def delete_message_after_delay(chat_id: int, message_id: int, delay_seconds: int = 60) -> None:
    """Удаляет сообщение через указанное время и чистит active_menus."""

    def _delete_message() -> None:
        time.sleep(delay_seconds)
        try:
            bot.delete_message(chat_id, message_id)
            # Удаляем из словаря активных меню
            current_id = active_menus.get(chat_id)
            if current_id == message_id:
                active_menus.pop(chat_id, None)
            logger.info("✅ Сообщение %s удалено", message_id)
        except Exception as e:
            logger.warning("❌ Не удалось удалить сообщение %s: %s", message_id, e)

    timer = threading.Thread(target=_delete_message, daemon=True)
    timer.start()


__all__ = ["active_menus", "delete_message_after_delay"]

