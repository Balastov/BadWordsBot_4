"""
Точка входа для бота.

Запускает экземпляр бота и регистрирует все обработчики.
"""

from bot_app import bot
from services.debug_runtime import debug_log

# Импортируем модули‑обработчики, чтобы декораторы выполнились при импорте
import handlers_main  # noqa: F401
import handlers_games  # noqa: F401
import handlers_admin  # noqa: F401
import handlers_stats  # noqa: F401
import handlers_bad_words  # noqa: F401
# region agent log
debug_log(
    hypothesis_id="H3",
    location="main.py:15",
    message="Handlers imported",
    data={"modules": ["handlers_main", "handlers_games", "handlers_admin", "handlers_stats", "handlers_bad_words"]},
)
# endregion


def main() -> None:
    # region agent log
    debug_log(
        hypothesis_id="H1",
        location="main.py:22",
        message="Starting polling loop",
        data={"none_stop": True},
    )
    # endregion
    try:
        bot.polling(none_stop=True)
    except Exception as exc:
        # region agent log
        debug_log(
            hypothesis_id="H1",
            location="main.py:30",
            message="Polling crashed with exception",
            data={"error_type": type(exc).__name__, "error_text": str(exc)},
        )
        # endregion
        raise


if __name__ == "__main__":
    main()

