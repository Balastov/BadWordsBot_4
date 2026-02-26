import logging

import telebot

from bot_app import bot
from services.menu_service import active_menus, delete_message_after_delay


logger = logging.getLogger(__name__)


@bot.message_handler(func=lambda message: message.text == "Играть в кампуктер")
def play_computer_menu(message) -> None:
    """Показывает меню выбора игры."""
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    btn1 = telebot.types.InlineKeyboardButton(
        "Paladins", callback_data="game_paladins"
    )
    btn2 = telebot.types.InlineKeyboardButton(
        "Supreme Commander", callback_data="game_supreme_commander"
    )
    btn3 = telebot.types.InlineKeyboardButton("Гоночки", callback_data="game_races")
    btn4 = telebot.types.InlineKeyboardButton(
        "Satisfactory", callback_data="game_satisfactory"
    )
    btn5 = telebot.types.InlineKeyboardButton(
        "Ascent", callback_data="game_ascent"
    )
    btn6 = telebot.types.InlineKeyboardButton(
        "Другая игра", callback_data="game_empty"
    )

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

    sent_message = bot.send_message(
        message.chat.id,
        "*Ну что, юный (или не очень) задрот, во что ты собрался поиграть?*"
        "\n\n*Сообщение удалится через минуту, не втыкай!* ⏰",
        reply_markup=markup,
        parse_mode="Markdown",
    )

    # Сохраняем ID сообщения
    active_menus[message.chat.id] = sent_message.message_id

    # Запускаем таймер удаления
    delete_message_after_delay(message.chat.id, sent_message.message_id, 60)


@bot.callback_query_handler(func=lambda call: call.data.startswith("game_"))
def handle_game_selection(call) -> None:
    """Обработчик выбора игры в inline‑меню."""
    try:
        games = {
            "game_paladins": (
                "@mr_clown_baban, @Balastov, @utka_uwu, @ongad, "
                "@Lobok000, @zloifikyc, @sheynnette, погнали играть в Pasasins!"
            ),
            "game_supreme_commander": (
                "Погнали играть в Supreme Commander!\n"
                "Не забудь зареклеймить масс-экстрактор у союзника =)\n"
                "@mr_clown_baban, @Balastov, @ongad, @Lobok000, @zloifikyc"
            ),
            "game_races": (
                "Погнали в какие-нибудь гоночки?\n"
                "@Balastov, @ongad, @Lobok000, проверьте масло и давление в шинах!"
            ),
            "game_satisfactory": (
                "😳😳😳\nЕЕЕЕЕЕЕЕЕЕЕЕЕЕБААААААААТЬ!!!\n"
                "ОООООООООХУЕЕЕЕЕЕЕЕЕЕТЬ!!!\n"
                "Срочно @Balastov буди Геннадия, время выплавлять ебучий алюминий!"
            ),
            "game_ascent": (
                "Погнали в Ascent, @Balastov, @ongad, @Lobok000, @mr_clown_baban"
            ),
            "game_empty": "Здесь пока пусто",
        }

        # Удаляем меню сразу при выборе игры
        chat_id = call.message.chat.id
        menu_id = active_menus.get(chat_id)
        if menu_id:
            try:
                bot.delete_message(chat_id, menu_id)
            except Exception:
                pass
            finally:
                active_menus.pop(chat_id, None)

        bot.send_message(chat_id, games.get(call.data, "Здесь пока пусто"))
        bot.answer_callback_query(call.id, "Народ вызван, можешь спокойно курить")

    except Exception as e:
        logger.error("❌ Ошибка в обработчике игр: %s", e)
        bot.answer_callback_query(call.id, "АШЫПКА!")


# Текстовые кнопки игр (альтернативный вариант, оставляем для обратной совместимости)


@bot.message_handler(func=lambda message: message.text == "Paladins")
def paladins_action(message) -> None:
    bot.send_message(message.chat.id, "")


@bot.message_handler(func=lambda message: message.text == "Supreme Commander")
def supreme_action(message) -> None:
    bot.send_message(
        message.chat.id,
        "🤖 Ты прекрасен! Играть в стратегии - это тебе не бэбру у Макоа нюхать.\n"
        "Не забудь зареклеймить масс-экстрактор у союзника, "
        "иначе в этом всём нет никакого смысла.\n"
        "@mr_clown_baban @Balastov @ongad @Lobok000 @zloifikyc",
    )


@bot.message_handler(func=lambda message: message.text == "Гоночки")
def races_action(message) -> None:
    bot.send_message(
        message.chat.id,
        "🚗 Тормоза придумали трусы! Как хочешь, так и интерпретируй эту фразу.\n"
        "В любом случае пора собирать команду. Я знаю, что здесь есть любители погонять - "
        "@Balastov @ongad @Lobok000, проверьте масло и давление в шинах!",
    )


@bot.message_handler(func=lambda message: message.text == "Satisfactory")
def satisfactory_action(message) -> None:
    bot.send_message(
        message.chat.id,
        "😳😳😳\nЕЕЕЕЕЕЕЕЕЕЕЕЕЕБААААААААТЬ!!!\n"
        "ОООООООООХУЕЕЕЕЕЕЕЕЕЕТЬ!!!\n"
        "Срочно @Balastov буди Геннадия, время выплавлять ебучий алюминий!",
    )

