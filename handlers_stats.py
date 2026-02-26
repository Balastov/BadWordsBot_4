import logging
from datetime import datetime

from bot_app import bot
from services.menu_service import active_menus, delete_message_after_delay
from services.stats_service import (
    get_bad_top,
    get_sticker_top,
    get_user_sticker_stats,
)


logger = logging.getLogger(__name__)


@bot.message_handler(func=lambda message: message.text == "Статистика")
def stats_menu(message) -> None:
    """Показывает меню статистики."""
    from telebot import types

    markup = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton("Стикеры общее", callback_data="sticker_stats")
    btn2 = types.InlineKeyboardButton("Стикеры топ", callback_data="sticker_top")
    btn3 = types.InlineKeyboardButton(
        "Матершинники топ", callback_data="bad_words_top"
    )

    markup.add(btn1, btn2, btn3)

    sent_message = bot.send_message(
        message.chat.id,
        "*По данным статистики данные статистики часто пиздят.*"
        "\n\n*Сообщение удалится через минуту, не втыкай!* ⏰",
        reply_markup=markup,
        parse_mode="Markdown",
    )

    active_menus[message.chat.id] = sent_message.message_id
    delete_message_after_delay(message.chat.id, sent_message.message_id, 60)


@bot.callback_query_handler(
    func=lambda call: call.data in ["sticker_stats", "sticker_top", "bad_words_top"]
)
def handle_statistics_buttons(call) -> None:
    """Обработчик inline‑кнопок статистики."""
    try:
        chat_id = call.message.chat.id

        if call.data == "sticker_stats":
            user_stats = get_user_sticker_stats(call.from_user.id, chat_id)

            response = "📊 Твоя статистика стикеров:\n"
            response += f"🎭 Количество: {user_stats['sticker_count']} шт.\n"

            last_date = user_stats.get("last_sticker_date")
            if isinstance(last_date, datetime):
                response += (
                    f"🕒 Последний: {last_date.strftime('%d.%m.%Y %H:%M')}"
                )

            bot.send_message(chat_id, response)

        elif call.data == "sticker_top":
            top_users, total_stickers = get_sticker_top(chat_id, limit=3)

            if not top_users:
                bot.send_message(
                    chat_id, "📭 В этом чате еще нет стикеров!"
                )
            else:
                response = "🏆 ТОП стикерменов:\n\n"

                for i, (username, first_name, last_name, count) in enumerate(
                    top_users, 1
                ):
                    display_name = (
                        f"{username}"
                        if username
                        else f"{first_name} {last_name or ''}".strip()
                    )
                    response += f"{i}. {display_name} - {count} стикеров\n"

                response += (
                    f"\n📦 Всего стикеров в чате: {total_stickers or 0}"
                )
                bot.send_message(chat_id, response)

        elif call.data == "bad_words_top":
            top_users = get_bad_top(chat_id, limit=15)

            if not top_users:
                bot.send_message(
                    chat_id,
                    "Все какие-то соевые.. Фу, аж противно! 🤢",
                )
            else:
                response = "🏆 ТОП матершинников:\n\n"

                for i, (username, first_name, last_name, score) in enumerate(
                    top_users, 1
                ):
                    display_name = (
                        f"{username}"
                        if username
                        else f"{first_name} {last_name or ''}".strip()
                    )
                    response += f"{i}. {display_name} - {score} баллов\n"

                bot.send_message(chat_id, response)

        bot.answer_callback_query(call.id, "Статистика показана!")

    except Exception as e:
        logger.error("❌ Ошибка обработки статистики: %s", e)
        bot.answer_callback_query(call.id, "Ошибка!")


@bot.message_handler(func=lambda message: message.text == "Матершинники топ")
def show_bad_top(message) -> None:
    """Текстовая команда для показа топа матершинников."""
    chat_id = message.chat.id
    top_users = get_bad_top(chat_id, limit=15)

    if not top_users:
        bot.reply_to(
            message,
            "Все какие-то соевые.. Фу, аж противно! 🤢",
        )
        return

    response = "🏆 ТОП матершинников:\n\n"

    for i, (username, first_name, last_name, score) in enumerate(
        top_users, 1
    ):
        display_name = (
            f"{username}"
            if username
            else f"{first_name} {last_name or ''}".strip()
        )
        response += f"{i}. {display_name} - {score} баллов\n"

    bot.reply_to(message, response)

