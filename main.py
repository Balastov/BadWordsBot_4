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
    restart_count = 0
    while True:
        restart_count += 1
        # region agent log
        debug_log(
            hypothesis_id="H1",
            location="main.py:25",
            message="Starting polling loop",
            data={
                "restart_count": restart_count,
                "mode": "infinity_polling",
            },
        )
        # endregion
        try:
            bot.infinity_polling(
                timeout=20,
                long_polling_timeout=20,
                skip_pending=False,
            )
        except Exception as exc:
            # region agent log
            debug_log(
                hypothesis_id="H1",
                location="main.py:41",
                message="Polling crashed with exception; restarting",
                data={
                    "restart_count": restart_count,
                    "error_type": type(exc).__name__,
                    "error_text": str(exc),
                },
            )
            # endregion


if __name__ == "__main__":
    main()

