import logging

import telebot

from bot_app import bot, daily_events, meme_sender, sticker_counter
from services.jokes_service import get_random_joke
from services.users_repository import init_users_db


logger = logging.getLogger(__name__)


# Инициализируем базу пользователей при старте приложения
init_users_db()


def show_main_menu(chat_id: int, message_text: str = "🤖 Главное меню") -> None:
    """Показывает главное меню."""
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton("Admin")
    btn2 = telebot.types.KeyboardButton("Играть в кампуктер")
    btn3 = telebot.types.KeyboardButton("Start Events")
    btn4 = telebot.types.KeyboardButton("Шутка за 300")
    btn5 = telebot.types.KeyboardButton("Статистика")
    btn6 = telebot.types.KeyboardButton("🎬 Мемы")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

    bot.send_message(chat_id, message_text, reply_markup=markup)


@bot.message_handler(commands=["start"])
def handle_start(message) -> None:
    """Запуск бота."""
    # Автоматически запускаем ежедневные события и мемы
    daily_events.start_daily_scheduler(message.chat.id)
    meme_sender.start_meme_scheduler(message.chat.id)

    show_main_menu(message.chat.id, "🤖 Главное меню:")
    bot.send_message(
        message.chat.id,
        "✅ Запущены ежедневные события и мемы, держите шорты!",
    )


@bot.message_handler(commands=["start_events"])
def start_daily_events_command(message) -> None:
    """Команда для запуска ежедневных событий."""
    daily_events.start_daily_scheduler(message.chat.id)
    bot.reply_to(
        message,
        "✅ Ежедневные события запущены! Буду присылать в 8:00 по МСК",
    )


@bot.message_handler(commands=["events"])
def send_events_now_command(message) -> None:
    """Ручная отправка событий."""
    daily_events.send_daily_event(message.chat.id)


@bot.message_handler(commands=["start_memes"])
def start_memes_command(message) -> None:
    """Команда для запуска отправки мемов по расписанию."""
    meme_sender.start_meme_scheduler(message.chat.id)
    bot.reply_to(
        message,
        "✅ Мемы активированы! Буду отправлять в 9:00, 15:00 и 20:00 по МСК",
    )


@bot.message_handler(commands=["stop_memes"])
def stop_memes_command(message) -> None:
    """Команда для остановки отправки мемов по расписанию."""
    meme_sender.stop_meme_scheduler()
    bot.reply_to(message, "🛑 Мемы отключены")


@bot.message_handler(commands=["meme"])
def send_meme_now_command(message) -> None:
    """Команда для немедленной отправки мема."""
    bot.send_chat_action(message.chat.id, "upload_photo")
    meme_sender.send_meme_now(message.chat.id)
    bot.reply_to(message, "Ололо! Мем отправлен!")


@bot.message_handler(func=lambda message: message.text == "Start Events")
def start_daily_events_button(message) -> None:
    """Кнопка в меню для запуска ежедневных событий."""
    daily_events.start_daily_scheduler(message.chat.id)
    bot.reply_to(
        message,
        "✅ Ехало! Буду присылать праздники каждый день в 8:00 по МСК. Инджой.",
    )


@bot.message_handler(func=lambda message: message.text == "Шутка за 300")
def send_joke(message) -> None:
    """Отправка случайного анекдота по кнопке."""
    try:
        bot.send_chat_action(message.chat.id, "typing")
        joke = get_random_joke()
        bot.reply_to(message, f"Ехало:\n\n{joke}")
    except Exception as e:
        logger.error("Ошибка при отправке анекдота: %s", e)
        bot.reply_to(
            message,
            "Чёт, сука, не находится шутейка... Анлак((",
        )


@bot.message_handler(func=lambda message: message.text == "🎬 Мемы")
def send_meme_from_menu(message) -> None:
    """Отправляет случайный мем при нажатии кнопки."""
    bot.send_chat_action(message.chat.id, "upload_photo")
    meme_sender.send_meme_now(message.chat.id)


@bot.message_handler(func=lambda message: message.text == "🔙 Назад")
def back_to_main_menu(message) -> None:
    """Возврат в главное меню из любых подменю."""
    show_main_menu(message.chat.id, "🤖 Главное меню:")


@bot.message_handler(content_types=["sticker"])
def handle_sticker(message) -> None:
    """Обработчик стикеров — считает количество отправленных стикеров."""
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        chat_id = message.chat.id

        sticker_counter.add_sticker(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            chat_id=chat_id,
        )
    except Exception as e:
        logger.error("Ошибка при обработке стикера: %s", e)



