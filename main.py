"""
Точка входа для бота.

Запускает экземпляр бота и регистрирует все обработчики.
"""

from bot_app import bot

# Импортируем модули‑обработчики, чтобы декораторы выполнились при импорте
import handlers_main  # noqa: F401
import handlers_games  # noqa: F401
import handlers_admin  # noqa: F401
import handlers_stats  # noqa: F401
import handlers_bad_words  # noqa: F401


def main() -> None:
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()

