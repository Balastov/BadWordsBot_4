import logging

import telebot

from bot_app import bot
from handlers_main import show_main_menu
from services.users_repository import add_user_to_db, get_chat_users


logger = logging.getLogger(__name__)


@bot.message_handler(func=lambda message: message.text == "Admin")
def admin_menu(message) -> None:
    """Показывает подменю Admin."""
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton("add_admins")
    btn2 = telebot.types.KeyboardButton("add_user")
    btn3 = telebot.types.KeyboardButton("show_users")
    btn4 = telebot.types.KeyboardButton("auto_collect_users")
    btn_back = telebot.types.KeyboardButton("🔙 Назад")

    markup.add(btn1, btn2, btn3, btn4, btn_back)

    bot.send_message(
        message.chat.id,
        "Сюда нельзя, козлёночком станешь!",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "add_admins")
def add_all_users_command(message) -> None:
    """Добавляет администраторов чата в базу пользователей."""
    try:
        chat_members = bot.get_chat_administrators(message.chat.id)

        added_count = 0
        for member in chat_members:
            user = member.user
            if add_user_to_db(
                user.id,
                user.username,
                user.first_name,
                user.last_name,
                message.chat.id,
            ):
                added_count += 1

        bot.reply_to(message, f"✅ Добавлено {added_count} пользователей в базу")

    except Exception as e:
        logger.error("❌ Ошибка при добавлении всех пользователей: %s", e)
        bot.reply_to(message, "❌ Не удалось добавить пользователей")


@bot.message_handler(func=lambda message: message.text == "add_user")
def add_user_command(message) -> None:
    """Добавляет отправителя команды в базу пользователей."""
    user = message.from_user
    success = add_user_to_db(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        chat_id=message.chat.id,
    )

    if success:
        bot.reply_to(
            message,
            f"✅ Пользователь @{user.username or user.first_name} добавлен в базе",
        )
    else:
        bot.reply_to(message, "❌ Не удалось добавить пользователя")


@bot.message_handler(func=lambda message: message.text == "show_users")
def show_users_command(message) -> None:
    """Показывает всех пользователей чата из базы."""
    users = get_chat_users(message.chat.id)

    if not users:
        bot.reply_to(message, "📭 В базе нет пользователей этого чата")
        return

    response = "👥 Пользователи чата:\n\n"

    for i, (user_id, username, first_name, last_name, chat_id) in enumerate(
        users, 1
    ):
        user_info = (
            f"{username}" if username else f"{first_name} {last_name or ''}".strip()
        )
        response += f"{i}. {user_info} (ID: {user_id})\n"

    bot.reply_to(message, response)


@bot.message_handler(func=lambda message: message.text == "auto_collect_users")
def auto_collect_users_button(message) -> None:
    """Плейсхолдер‑кнопка для debug."""
    bot.send_message(message.chat.id, "=))))")

