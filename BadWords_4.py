# 7856651931:AAGkiOiF964M_AcjfCsheAHXXQ5dfC0rXB4
import random
from http.client import responses

from datetime import datetime
import telebot
from bs4 import BeautifulSoup
import requests
import sqlite3
import threading
import time

# from telegram._utils import markup

from DailyEvents import DailyEvents
from StickerCounter import StickerCounter
# from QuestionsSender import QuestionsSender
# from MemeSender import MemeSender
# import os

# import random

# from telegram._utils import markup

bot = telebot.TeleBot('8384870189:AAEViu4Ee_0jD6-SU7F6TQMHIJCLUyT-SI4')
daily_events = DailyEvents(bot)
sticker_counter = StickerCounter()

# тест 2
#-------------------------------------------------------------------------------------------------------------------

try:
    from BadScore_1 import increase_bad_score, get_bad_score, get_top_bad_scores
except ImportError:
    print("⚠️ Модуль BadScore_1 не найден, используем заглушки")


    # Заглушки на случай если модуль не найден
    def increase_bad_score(user_id, username, first_name, last_name, chat_id):
        return 1


    def get_bad_score(user_id, chat_id):
        return 0


    def get_top_bad_scores(chat_id, limit=10):
        return []

#-------------------------------------------------------------------------------------------------------------------




bot_answer_testButton = ['Не жми, блядь, ничего!', 'Отвали от кнопок!',
                    'Ещё не работает!', 'Перерыв на обед', 'Пойди, Кефиру пожалуйся'
                    ]


bot_answer_bad_words = ['Фу, как некультурно!', 'И ты этими губами мороженку хаваешь?!',
                    'По жопе пора тебе прописать!', 'Вымой рот с мылом и пальцы тоже.',
                    'Даже @zloifikyc такого себе не позволяет!', "Заебал, блядь, материться, сука!",
                    "В ёбыч прописать? Не ругайся!", "Давайте жить дружно!",
                    "Что легче - килограмм пуха или килограмм гвоздей?",
                    "Каков шанс, что ты ебанутая?\nНемалый!", "Материться здесь можно только мне.",
                    "Не каждый глобальный индивидуум со стороны парадоксальных тенденций может понять концепцию "
                    "адекватного восприятия реальной действительности", "Ебучие пироги, ты чё творишь?!",
                    "Достаточно.", "Я обожаю, когда в ролике с рекламой монитора нам показывают, какие у него яркие"
                                   " цвета. А если мы эти яркие цвета видим на своих мониторах, то "
                                   "НАХУЯ нам новый?!",
                    "Самое лучшее время для совершения преступлений в Готем-Сити это безоблачная ночь =)",
                    "Пиздеть команды не было.", "Я его рот наоборот, а ты не ругайся.",
                    "Зачастил, братан, зачастил...",
                    "Верните Кефира, хули он там сидит в своей Террарии? Отхуесосить некого..",
                    "Ты уже продал тот розовый дилдак?", "И восстали машины из пепла ядерного огня...",
                    "Пойди, книжку почитай.", "Я есть Грут!", "Ootka peedor", "Мальчик гей, будь со мной понаглей",
                    "Немало: немецкий автономный округ.", "А я напоминаю, что наказание для топового матершинника - "
                                                          "месяц играть в Satisfactory с Квазаром"
                        ]

bot_replay_answer_bad_words = ["Ах ты, хуила! Ещё и огрызаешься! Ну, пиздец тебе.", "Давай, попизди мне тут))",
                               "Ты вообще понимаешь, что сам себя закапываешь?",
                               "Смотрю, причинно-следственные связи - это вообще не твоё...",
                               "Тебе русским языком сказали, чурка ебаная, соблюдай правила приличия!",
                               "А, ну тогда ладно...", "А если уебать и переспросить?"

]

ballov_nemalo = ["А сколько там у тебя баллов накопилось? Немало, уже ",
                 "Тебя отхуесосили за мат примерно раз ",
                 "Твой счёт - ", "Количество твоих баллов - ",
                 "У тебя баллов ровно столько, сколько ты раз смотрел Сумерки. А именно - ",
                 "Фууууууу, а баллов-то уже "

]

bot_answer_no = ["Пидора ответ", "Хипстора планшет", "Гомогея ответ", "Голый пистолет", "В Турцию билет",
                 "Сам знаешь, чей ответ", "Розовый берет", "Скользкий парапет", "Чайковского балет",
                 "Группа Nazareth", "От Дилдоджона привет", "Вагон-кабриолет"
]

bot_answer_no_ukr = [
     "Пидора отвэ", "Ай нанэ нанэ", "Всё ебло в говнэ"
]

bot_answer_yes = ["Пизда!"]


bot_answer_aga = ["В жопе нога", "Врага! Пока лежит, а то убежит!"]

exeptions = [
    "требует", "требуют", "требование", "требования",
    "херсон", "херувим", "херувимы", "требует",
    "педиатр", "педиатрия", "педикюр",
    "мандарин", "мандарины", "мандариновый",
    "пизон", "пизоны",  # если есть такое слово
    "страхуй", "страхуйте",  # страхуй как финансовый термин
    "перестрахуй", "перестрахование", "рубля", "требуют", "требуются", "требует", "требуется",
    "употреблять", "оскорблять", "ребут"
]

bad_words = ["хуй", "хyй", "xyй", "хуёвый", "хуевый", "хуёвые", "хуевая", "хуёвая", "хуя", "хуета", "х у й", "п и з д а",
    "хуевые", "хуёвые", "нахуевертить", "хуишко", "хууй", "хуууй", "хууууй", "хуууууй", "хууууууй", "хуле",
    "ахуел", "хуила", "ахуена", "ахуено", "ахуен", "охуен", "ахуит", "охуит",
    "пизда", "песда", "песдец", "пиздец", "пиздатый", "пиздатая", "пиздюлина", "пизды",
    "пиздюлины", "пиздюлину", "пиздюлин", "пиздюлей", "пиздюк", "песдюк", "пизду", "пиздуй", "пиздуешь",
    "пзду", "опездал", "опездол", "шопиздец", "пиздит", "напиздел",
    "ебанутый", "ебанашка", "ебан", "йбал", "ебобаный", "ебобаных", "ебобаная", "уебище",
    "ебанашки", "ебанашке", "ебанашку", "ебанутая", "ебанутой", "ебанутые", "ебашит",
    "наебенился", "ебашь", "выеби", "проебывал", "проёбина", "проебина", "проёб", "проеб",
    "ебанутую", "ебанутого", "йобаный", "ебать", "ебу", "ебал", "наебовертить", "долбоёб", "долбоеб",
    "долбаеб", "разъёб", "наёбан", "наебан", "е б а т ь", "еблан", "сьебал", "еблуш", "уёбищ", "уёбок",
    "уебок", "уёб",
    "охуенный", "охуенная", "хуила", "охуел", "охуеть", "ахуенно",
    "охуенное", "охуенные", "хуесос", "хуесосы", "ахуеть", "охуеть", "хер", "херовый", "херовая", "херовые",
    "бля", "блядь", "блять", "блядина", "блядин", "блядину", "пидор", "пидар", "пидорас", "пидарас", "педрила",
    "пидрила", "пидр", "ебальник", "ебало", "ёбла", "гандон", "гондон", "шлюха", "залупа",
    "манда", "членосос",
    "педик", "говноед",
    "дрочить", "дрочил", "задрочил"
             ]



#---------------------------------------------------------------------------------------------------------------


# Создание таблицы пользователей
# Инициализация базы данных пользователей
def init_users_db():
    try:
        conn = sqlite3.connect('users_database.sqlite')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_users (
            user_id INTEGER,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            chat_id INTEGER,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, chat_id)
        )
        ''')

        conn.commit()
        conn.close()
        print("✅ База данных пользователей создана")

    except Exception as e:
        print(f"❌ Ошибка при создании базы пользователей: {e}")


# Инициализируем при запуске
init_users_db()



# Функция добавления пользователя
def add_user_to_db(user_id, username, first_name, last_name, chat_id):
    try:
        conn = sqlite3.connect('users_database.sqlite')
        cursor = conn.cursor()

        # Сначала проверяем существует ли пользователь
        cursor.execute('''
        SELECT 1 FROM chat_users 
        WHERE user_id = ? AND chat_id = ?
        ''', (user_id, chat_id))

        existing_user = cursor.fetchone()

        if existing_user:
            print(f"ℹ️ Пользователь {username or first_name} уже существует в базе")
            conn.close()
            return False

        # Если пользователя нет - добавляем
        cursor.execute('''
        INSERT INTO chat_users 
        (user_id, username, first_name, last_name, chat_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, chat_id))

        conn.commit()
        conn.close()
        print(f"✅ Пользователь {username or first_name} добавлен в базу")
        return True

    except Exception as e:
        print(f"❌ Ошибка при добавлении пользователя: {e}")
        return False

# Функция получения всех пользователей чата
def get_chat_users(chat_id):
    try:
        conn = sqlite3.connect('users_database.sqlite')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT user_id, username, first_name, last_name, chat_id
        FROM chat_users 
        WHERE chat_id = ?
        ORDER BY first_name
        ''', (chat_id,))

        users = cursor.fetchall()
        conn.close()
        return users

    except Exception as e:
        print(f"❌ Ошибка при получении пользователей: {e}")
        return []


# Функция для проверки наличия пользователя в базе
def is_user_in_db(user_id, chat_id):
    try:
        conn = sqlite3.connect('users_database.sqlite')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT 1 FROM chat_users 
        WHERE user_id = ? AND chat_id = ?
        ''', (user_id, chat_id))

        result = cursor.fetchone()
        conn.close()

        return result is not None  # True если пользователь найден

    except Exception as e:
        print(f"❌ Ошибка при проверке пользователя: {e}")
        return False  # В случае ошибки считаем что пользователя нет


# Модифицируем функцию для сбора пользователей из сообщений
def auto_collect_users(message):
    user = message.from_user
    # Проверяем не бот ли это
    if not user.is_bot:
        # Проверяем есть ли пользователь уже в базе
        if not is_user_in_db(user.id, message.chat.id):
            add_user_to_db(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                chat_id=message.chat.id
            )
            print(f"✅ Добавлен новый пользователь: {user.username or user.first_name}")
        else:
            print(f"ℹ️ Пользователь уже в базе: {user.username or user.first_name}")


# ----------------------------------------------------------------

def should_bot_reply(probability=0.20, debug=False):
    """
    Определяет, должен ли бот ответить с заданной вероятностью

    Args:
        probability (float): Вероятность ответа от 0.0 до 1.0
        debug (bool): Включить логирование

    Returns:
        bool: True если бот должен ответить, False если промолчать
    """
    chance = random.random()
    should_reply = chance <= probability

    if debug:
        status = "✅ ОТВЕТ" if should_reply else "🔇 МОЛЧАНИЕ"
        print(f"🎲 Вероятность ответа: {chance:.2f} <= {probability} -> {status}")

    return should_reply

def bot_reply_with_probability(message, response_text, probability=0.20, debug=True):
    """
        Отправляет ответ с заданной вероятностью

        Args:
            message: Объект сообщения от telebot
            response_text (str): Текст ответа
            probability (float): Вероятность отправки ответа
            debug (bool): Включить логирование

        Returns:
            bool: True если ответ отправлен, False если промолчал
        """
    if should_bot_reply(probability, debug):
        bot.reply_to(message, response_text)
        if debug:
            print(f"🗣️ Бот ответил (шанс {probability*100}%): {response_text[:50]}...")
        return True
    else:
        if debug:
            print(f"🔇 Бот промолчал (шанс {probability*100}%)")
        return False







#-----------------------------------------------------------------






# Единая функция главного меню
def show_main_menu(chat_id, message_text="🤖 Главное меню"):
    """Показывает главное меню"""
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton('Admin')
    btn2 = telebot.types.KeyboardButton('Играть в кампуктер')
    btn3 = telebot.types.KeyboardButton('Start Events')
    #btn4 = telebot.types.KeyboardButton('Перепись матершинников')
    btn4 = telebot.types.KeyboardButton('Шутка за 300')
    btn5 = telebot.types.KeyboardButton('Статистика')

    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(chat_id, message_text, reply_markup=markup)

#--------------------------------------------------------------------------------------------------------------










#---------------------------------------------------------------------------------------------------------------







# Проверка наличия матерных слов в тексте
def contains_bad_words(text):
    if not text or not isinstance(text, str):
        return False

    text_lower = text.lower()

    # Сначала проверяем исключения - если слово есть в исключениях, пропускаем
    words = text_lower.split()
    for word in words:
        if word in exeptions:
            return False

    # Затем проверяем матерные слова
    return any(bad_word in text_lower for bad_word in bad_words)

@bot.message_handler(commands=['start'])
def handle_start(message):
    show_main_menu(message.chat.id, "🤖 Главное меню:")

# Команда для запуска ежедневных событий
@bot.message_handler(commands=['start_events'])
def start_daily_events(message):
    daily_events.start_daily_scheduler(message.chat.id)
    bot.reply_to(message, "✅ Ежедневные события запущены! Буду присылать в 8:00 по МСК")

# Команда для ручной проверки
@bot.message_handler(commands=['events'])
def send_events_now(message):
    daily_events.send_daily_event(message.chat.id)

@bot.message_handler(func=lambda message: message.text == 'Admin')
def test_menu(message):
    # Создаём выпадающее меню для Admin
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    # Добавляем кнопки подменю Admin
    btn1 = telebot.types.KeyboardButton('add_admins')
    btn2 = telebot.types.KeyboardButton('add_user')
    btn3 = telebot.types.KeyboardButton('show_users')
    btn4 = telebot.types.KeyboardButton('auto_collect_users')
    btn_back = telebot.types.KeyboardButton('🔙 Назад')

    markup.add(btn1, btn2, btn3, btn4, btn_back)

    # Отправляем сообщение с подменю
    bot.send_message(message.chat.id, "Сюда нельзя, козлёночком станешь!", reply_markup=markup)


# Словарь для хранения ID сообщений с меню
active_menus = {}

# Обработчик стикеров
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    """Обработчик стикеров"""
    try:
        user = message.from_user
        sticker = message.sticker

        #Добавляем стикер в счётчик
        sticker_count = sticker_counter.add_sticker(
            user_id = user.id,
            username = user.username,
            first_name = user.first_name,
            last_name = user.last_name,
            chat_id = message.chat.id,
            sticker_id = sticker.file_id,
        )

        # Можно добавить ответ с вероятностью (опционально)
        if sticker_count and sticker_count % 10 == 0:  # Каждые 10 стикеров
            username = f"@{user.username}" if user.username else user.first_name
            response = f"🎉 {username}, ты отправил уже {sticker_count} стикеров!"
            bot_reply_with_probability(message, response, 0.30)  # 30% шанс ответа

        print(f"📎 Стикер от {user.username or user.first_name}: {sticker_count} шт.")

    except Exception as e:
        print(f"❌ Ошибка обработки стикера: {e}")

def delete_message_after_delay(chat_id, message_id, delay_seconds=60):
    """Удаляет сообщения через указанное время"""

    def delete_message():
        time.sleep(delay_seconds)
        try:
            bot.delete_message(chat_id, message_id)
            # Удаляем из словаря активных меню
            if chat_id in active_menus:
                del active_menus[chat_id]
            print(f"✅ Сообщение {message_id} удалено")
        except Exception as e:
            print(f"❌ Не удалось удалить сообщение: {e}")

    timer = threading.Thread(target=delete_message)
    timer.daemon = True
    timer.start()

@bot.message_handler(func=lambda message: message.text == 'Играть в кампуктер')
def play_сomputer_menu(message):
    # Создаём выпадающее меню для "Играть в кампуктер"
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    # Добавляем кнопки подменю "Играть в кампуктер"
    btn1 = telebot.types.InlineKeyboardButton('Paladins', callback_data='game_paladins')
    btn2 = telebot.types.InlineKeyboardButton('Supreme Commander', callback_data='game_supreme_commander')
    btn3 = telebot.types.InlineKeyboardButton('Гоночки', callback_data='game_races')
    btn4 = telebot.types.InlineKeyboardButton('Satisfactory', callback_data='game_satisfactory')
    btn5 = telebot.types.InlineKeyboardButton('Ascent', callback_data='game_ascent')
    btn6 = telebot.types.InlineKeyboardButton('Другая игра', callback_data='game_empty')

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

    # Отправляем сообщение с подменю
    sent_message = bot.send_message(
        message.chat.id,
        "*Ну что, юный (или не очень) задрот, во что ты собрался поиграть?*"
        "\n\n*Сообщение удалится через минуту, не втыкай!* ⏰",
        reply_markup=markup,
        parse_mode='Markdown'
    )

    # Сохраняем ID сообщения
    active_menus[message.chat.id] = sent_message.message_id

    # Запускаем таймер удаления
    delete_message_after_delay(message.chat.id, sent_message.message_id, 60)


@bot.callback_query_handler(func=lambda call: call.data.startswith('game_'))
def handle_game_selection(call):
    try:
        games = {
            'game_paladins': "@mr_clown_baban, @Balastov, @utka_uwu, @ongad, @Lobok000, @zloifikyc, @sheynnette, "
                             "погнали играть в Pasasins!",
            'game_supreme_commander': f"Погнали играть в Supreme Commander!\n"
                                      "Не забудь зареклеймить масс-экстрактор у союзника =)\n"
                                      "@mr_clown_baban, @Balastov, @ongad, @Lobok000, @zloifikyc",
            'game_races': f"Погнали в какие-нибудь гоночки?\n"
                                      "@Balastov, @ongad, @Lobok000, проверьте масло и давление в шинах!",
            'game_satisfactory': f"😳😳😳\nЕЕЕЕЕЕЕЕЕЕЕЕЕЕБААААААААТЬ!!!\nОООООООООХУЕЕЕЕЕЕЕЕЕЕТЬ!!!\nСрочно "
                                      "@Balastov буди Геннадия, время выплавлять ебучий алюминий!",
            'game_ascent': f"Погнали в Ascent, @Balastov, @ongad, @Lobok000, @mr_clown_baban",
            'game_empty': f"Здесь пока пусто",
        }

        # Удаляем меню сразу при выборе игры
        if call.message.chat.id in active_menus:
            try:
                bot.delete_message(call.message.chat.id, active_menus[call.message.chat.id])
                del active_menus[call.message.chat.id]
            except:
                pass

        # Просто отправляем сообщение с вызовом игроков
        bot.send_message(call.message.chat.id, games[call.data])
        bot.answer_callback_query(call.id, "Народ вызван, можешь спокойно курить")

    except Exception as e:
        print(f'❌ Ошибка: {e}')
        bot.answer_callback_query(call.id, 'АШЫПКА!')








# Обработчики для кнопок меню
@bot.message_handler(func=lambda message: message.text == 'Admin')
# def start_cmd(message):
#     bot.send_message(message.chat.id, "Нажатие этой кнопки на данном этапе разработки имеет меньше смысла, "
#                                       "чем просмотр ТыкТока перед сном.")




# fix
@bot.message_handler(func=lambda message: message.text == 'Start Events')
# Команда для запуска ежедневных событий
def start_daily_events(message):
    daily_events.start_daily_scheduler(message.chat.id)
    bot.reply_to(message, "✅ Ехало! Буду присылать праздники каждый день в 8:00 по МСК. Инджой.")




# Обработчик команды /anekdot
@bot.message_handler(func=lambda message: message.text == 'Шутка за 300')
def send_joke(message):
    try:
        # Отправляем "печатает..." статус
        bot.send_chat_action(message.chat.id, 'typing')

        # Получаем анекдот
        joke = get_random_joke()

        # Отправляем анекдот
        bot.reply_to(message, f"Ехало:\n\n{joke}")

    except Exception as e:
        print(f"Ошибка при отправке анекдота: {e}")
        bot.reply_to(message, "Чёт, сука, не находится шутейка... Анлак((")




#------------------------------------------------------------------------------------------------
# Здесь кнопки для "Поиграть в кампуктер"

@bot.message_handler(func=lambda message: message.text == 'Paladins')
def test1_action(message):
    bot.send_message(message.chat.id, ""
                     )

@bot.message_handler(func=lambda message: message.text == 'Supreme Commander')
def supreme_action(message):
    bot.send_message(message.chat.id, "🤖 Ты прекрасен! Играть в стратегии - это тебе не бэбру у Макоа нюхать.\n"
                                      "Не забудь зареклеймить масс-экстрактор у союзника, "
                                      "иначе в этом всём нет никакого смысла.\n@mr_clown_baban @Balastov "
                                      "@ongad @Lobok000 @zloifikyc")

@bot.message_handler(func=lambda message: message.text == 'Гоночки')
def races_action(message):
    bot.send_message(message.chat.id, "🚗 Тормоза придумали трусы! Как хочешь, так и интерпретируй эту фразу.\nВ "
                                      "любом случае пора собирать команду. Я знаю, что здесь есть любители погонять - "
                                      "@Balastov @ongad @Lobok000, проверьте масло и давление в шинах!")

@bot.message_handler(func=lambda message: message.text == 'Satisfactory')
def satisfactory_action(message):
    bot.send_message(message.chat.id, "😳😳😳\nЕЕЕЕЕЕЕЕЕЕЕЕЕЕБААААААААТЬ!!!\nОООООООООХУЕЕЕЕЕЕЕЕЕЕТЬ!!!\nСрочно "
                                      "@Balastov буди Геннадия, время выплавлять ебучий алюминий!")


@bot.message_handler(func=lambda message: message.text == '🔙 Назад')
def back_from_games(message):
    show_main_menu(message.chat.id, "🤖 Главное меню:")
#--------------------------------------------------------------------------------------------
# Здесь админские кнопки

@bot.message_handler(func=lambda message: message.text == 'add_admins')
# Автоматически добавляем всех участников при команде в группе
def add_all_users_command(message):
    try:
        # Получаем информацию о чате
        chat_members = bot.get_chat_administrators(message.chat.id)

        added_count = 0
        for member in chat_members:
            user = member.user
            if add_user_to_db(user.id, user.username, user.first_name, user.last_name, message.chat.id):
                added_count += 1

        bot.reply_to(message, f"✅ Добавлено {added_count} пользователей в базу")

    except Exception as e:
        print(f"❌ Ошибка при добавлении всех пользователей: {e}")
        bot.reply_to(message, "❌ Не удалось добавить пользователей")


@bot.message_handler(func=lambda message: message.text == 'add_user')
# Команда для добавления пользователей
def add_user_command(message):
    # Добавляем отправителя команды
    user = message.from_user
    success = add_user_to_db(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        chat_id=message.chat.id
    )

    if success:
        bot.reply_to(message, f"✅ Пользователь @{user.username or user.first_name} добавлен в базу")
    else:
        bot.reply_to(message, "❌ Не удалось добавить пользователя")

@bot.message_handler(func=lambda message: message.text == 'show_users')
# Команда для показа всех пользователей
def show_users_command(message):
    users = get_chat_users(message.chat.id)

    if not users:
        bot.reply_to(message, "📭 В базе нет пользователей этого чата")
        return

    response = "👥 Пользователи чата:\n\n"

    for i, (user_id, username, first_name, last_name, chat_id) in enumerate(users, 1):
        user_info = f"{username}" if username else f"{first_name} {last_name or ''}".strip()
        response += f"{i}. {user_info} (ID: {user_id})\n"

    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: message.text == 'auto_collect_users')
def test_4_action(message):
    bot.send_message(message.chat.id, "=))))")


@bot.message_handler(func=lambda message: message.text == '🔙 Назад')
def back_from_admin(message):
    show_main_menu(message.chat.id, "🤖 Главное меню:")


#--------------------------------------------------------------------------------------------
# Здесь кнопки для статистики

@bot.message_handler(func=lambda message: message.text == 'Статистика')
def play_сomputer_menu(message):
    # Создаём выпадающее меню для "Статистика"
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    # Добавляем кнопки подменю "Статистика"
    btn1 = telebot.types.InlineKeyboardButton('Стикеры общее', callback_data='stats_stickers')
    btn2 = telebot.types.InlineKeyboardButton('Стикеры топ', callback_data='stats_sticker_top')
    btn3 = telebot.types.InlineKeyboardButton('Матершинники топ', callback_data='stats_bad_words_top')

    markup.add(btn1, btn2, btn3)

    # Отправляем сообщение с подменю
    sent_message = bot.send_message(
        message.chat.id,
        "*По данным статистики данные статистики часто пиздят*"
        "\n\n*Сообщение удалится через минуту, не втыкай!* ⏰",
        reply_markup=markup,
        parse_mode='Markdown'
    )


    # Сохраняем ID сообщения
    active_menus[message.chat.id] = sent_message.message_id

    # Запускаем таймер удаления
    delete_message_after_delay(message.chat.id, sent_message.message_id, 60)

# @bot.callback_query_handler(func=lambda call: call.data in ['stats_stickers', 'stats_sticker_top', 'stats_bad_words_top'])
# def show_sticker_stats(message):
#     """Показывает статистику стикеров пользователя"""
#     try:
#         if call.data == 'stats_stickers':
#             # Показываем статистику стикеров конкретного пользователя
#             user_stats = sticker_counter.get_sticker_stats(message.from_user.id, message.chat.id)
#
#             response = f"Твоя статистика стикеров:\n"
#             response += f" {user_stats['sticker_count']} шт.\n"
#
#             if user_stats['last_sticker_date']:
#                 last_date = datetime.fromisoformat(user_stats['last_sticker_date'])
#                 response += f"Последний: {last_date.strftime('%d.%m.%Y %H:%M')}"
#
#             bot.send_message(call.message.chat.id, response)
#
#         elif call.data == 'stats_sticker_top':
#             # Показываем топ стикеродрочеров
#             top_users = sticker_counter.get_top_sticker_users(call.message.chat.id, limit=10)
#             total_stickers = sticker_counter.get_total_stickers_in_chat(call.message.chat.id)
#
#                 if not top_users:
#                     bot.send_message(call.message.chat.id, 'В этом чате ещё нет зарегистрированных мной стикеров')
#                 else:
#                     response = f'ТОП стикероёбов:\n\n'
#
#                 for i, (username, first_name, last_name, count) in enumerate(top_users, 1):
#                     display_name = f"{username}" if username else f"{first_name} {last_name or ''}".strip()
#                 response += f"{i}. {display_name} - {count} стикеров\n"
#
#             response += f'Всего стикеров в чате: {total_stickers}'
#             bot.send_message(call.message.chat.id, response)
#
#         elif call.data == 'stats_bad_words_top':
#             # Показываем топ матершинников
#             top_users = get_top_bad_scores(call.message.chat.id, limit=15)
#
#             if not top_users:
#                 bot.send_message(call.message.chat.id, 'Фу, все такие культурные, аж противно')
#             else:
#                 response = 'ТОП матершинников:/n/n'
#
#             for i, (username, first_name, last_name, score) in enumerate(top_users, 1):
#                 display_name = f"{username}" if username else f"{first_name} {last_name or ''}".strip()
#                 response += f"{i}. {display_name} - количество баллов {score}\n"
#
#             bot.send_message(call.message.chat.id, response)
#
#         # Уведомляем пользователя, что кнопка нажата
#         bot.answer_callback_query(call.id, 'Вот статистика:')
#
#
#     except Exception as e:
#         print(f"❌ Ошибка показа статистики стикеров: {e}")
#         bot.reply_to(message, "❌ Не удалось получить статистику")

# @bot.message_handler(func=lambda message: message.text == 'Стикеры топ')
# def show_sticker_top(message):
#     """Показывает топ пользователей по стикерам"""
#     try:
#         top_users = sticker_counter.get_top_sticker_users(message.chat.id, limit=3)
#         total_stickers = sticker_counter.get_total_stickers_in_chat(message.chat.id)
#
#         if not top_users:
#             bot.reply_to(message, "📭 В этом чате еще нет стикеров!")
#             return
#
#         response = f"🏆 ТОП стикерменов:\n\n"
#
#         for i, (username, first_name, last_name, count) in enumerate(top_users, 1):
#             display_name = f"@{username}" if username else f"{first_name} {last_name or ''}".strip()
#             response += f"{i}. {display_name} - {count} стикеров\n"
#
#         response += f"\n📦 Всего стикеров в чате: {total_stickers}"
#
#         bot.reply_to(message, response)
#
#     except Exception as e:
#         print(f"❌ Ошибка показа топа стикеров: {e}")
#         bot.reply_to(message, "❌ Не удалось получить топ")

# Проблема в том, что вы создали inline-кнопки в меню "Статистика", но не добавили обработчик для callback'ов этих кнопок.
# Нужно добавить обработчик @bot.callback_query_handler для кнопок статистики
@bot.callback_query_handler(func=lambda call: call.data in ['sticker_stats', 'sticker_top', 'bad_words_top'])
def handle_statistics_buttons(call):
    try:
        if call.data == 'sticker_stats':
            # Показываем статистику стикеров пользователя
            user_stats = sticker_counter.get_sticker_stats(call.from_user.id, call.message.chat.id)

            response = f"📊 Твоя статистика стикеров:\n"
            response += f"🎭 Количество: {user_stats['sticker_count']} шт.\n"

            if user_stats['last_sticker_date']:
                response += f"🕒 Последний: {user_stats['last_sticker_date'].strftime('%d.%m.%Y %H:%M')}"

            bot.send_message(call.message.chat.id, response)

        elif call.data == 'sticker_top':
            # Показываем топ пользователей по стикерам
            top_users = sticker_counter.get_top_sticker_users(call.message.chat.id, limit=3)
            total_stickers = sticker_counter.get_total_stickers_in_chat(call.message.chat.id)

            if not top_users:
                bot.send_message(call.message.chat.id, "📭 В этом чате еще нет стикеров!")
            else:
                response = f"🏆 ТОП стикерменов:\n\n"

                for i, (username, first_name, last_name, count) in enumerate(top_users, 1):
                    display_name = f"@{username}" if username else f"{first_name} {last_name or ''}".strip()
                    response += f"{i}. {display_name} - {count} стикеров\n"

                response += f"\n📦 Всего стикеров в чате: {total_stickers}"
                bot.send_message(call.message.chat.id, response)

        elif call.data == 'bad_words_top':
            # Показываем топ матершинников
            top_users = get_top_bad_scores(call.message.chat.id, limit=15)

            if not top_users:
                bot.send_message(call.message.chat.id, "Все какие-то соевые.. Фу, аж противно! 🤢")
            else:
                response = "🏆 ТОП матершинников:\n\n"

                for i, (username, first_name, last_name, score) in enumerate(top_users, 1):
                    display_name = f"{username}" if username else f"{first_name} {last_name or ''}".strip()
                    response += f"{i}. {display_name} - {score} баллов\n"

                bot.send_message(call.message.chat.id, response)

        # Уведомляем пользователя что кнопка нажата
        bot.answer_callback_query(call.id, "Статистика показана!")

    except Exception as e:
        print(f"❌ Ошибка обработки статистики: {e}")
        bot.answer_callback_query(call.id, "Ошибка!")

#-----------------------------------------------------------------------------------------------




@bot.message_handler(func=lambda message: message.text == 'Матершинники топ')
# # Команда для показа топа нарушителей
# def show_bad_count(message):
#     if not users_scores:
#         bot.reply_to(message, "Все какие-то соевые.. Фу, аж противно! 🤢")
#         return
#
#     top_users = get_top_users_simple(limit=20)
#
#     response = "🏆 ТОП пиздоболов:\n\n"
#
#     for i, (username, first_name, last_name, score) in enumerate(top_users, 1):
#         display_name = f"@{username}" if username else f"{first_name} {last_name or ''}".strip()
#         response += f"{i}. {display_name} - {score} баллов\n"
#
#     bot.reply_to(message, response)

# Вариант с БД

# @bot.message_handler(commands=['bad_top'])
# Вот это я закомментировал последним
def show_bad_top(message):
    top_users = get_top_bad_scores(message.chat.id, limit=15)

    if not top_users:
        bot.reply_to(message, "Все какие-то соевые.. Фу, аж противно! 🤢")
        return

    response = "🏆 ТОП матершинников:\n\n"

    for i, (username, first_name, last_name, score) in enumerate(top_users, 1):
        display_name = f"{username}" if username else f"{first_name} {last_name or ''}".strip()
        response += f"{i}. {display_name} - {score} баллов\n"

    bot.reply_to(message, response)

# Конец варианта с БД


#--------------------------------------------------------------------------------------------

# Альтернативная простая версия без SQLite
users_scores = {}  # Вместо базы данных используем словарь


def update_user_score_simple(user_id, username, first_name, last_name):
    if user_id not in users_scores:
        users_scores[user_id] = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name or '',
            'score': 0
        }
    users_scores[user_id]['score'] += 1
    print(f"✅ Пользователь {username or first_name}: {users_scores[user_id]['score']} баллов")


def get_top_users_simple(limit=10):
    if not users_scores:
        return []

    sorted_users = sorted(users_scores.items(), key=lambda x: x[1]['score'], reverse=True)
    result = []

    for user_id, user_data in sorted_users[:limit]:
        result.append((
            user_data['username'],
            user_data['first_name'],
            user_data['last_name'],
            user_data['score']
        ))

    return result


# Проверка текста и ответ ---------------------------------


# 4. Обработчик матов
@bot.message_handler(func=lambda message: contains_bad_words(message.text))
def handle_bad_words(message):
    try:
        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name

        # ВСЕГДА увеличиваем счетчик
        new_score = increase_bad_score(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            chat_id=message.chat.id
        )

        # Проверяем, является ли сообщение ответом боту
        is_reply_to_bot = (
            message.reply_to_message and
            message.reply_to_message.from_user and
            message.reply_to_message.from_user.id == bot.get_me().id
        )

        # Выбираем фразы
        phrases = bot_replay_answer_bad_words if is_reply_to_bot else bot_answer_bad_words

        # Формируем ответ
        score_text = f"{random.choice(ballov_nemalo)} {new_score}!" if new_score is not None else ""
        bot_response = f"{username}, {random.choice(phrases)}\n{score_text}".strip()

        # ⚠️ ВАЖНО: используем bot_reply_with_probability вместо bot.reply_to
        bot_reply_with_probability(message, bot_response, 0.20)

    except Exception as e:
        print(f"❌ Ошибка в обработчике матов: {e}")


    # except Exception as e:
    #     print(f"❌ Ошибка в обработчике матов: {e}"))
    #     bot.reply_to(message, "Бля, что-то пошло не так... Анлак :'( ")


    # if new_score is not None:
    #     bot.reply_to(message, f"{username}, {random.choice(bot_answer_bad_words)}\n"
    #                               f"У тебя теперь {new_score} баллов.")
    # else:
    #     # Если произошла ошибка, используем альтернативный ответ
    #     bot.reply_to(message, f"{username}, Много болтаешь..")



# 5.1. Обработчик слова "нет"
@bot.message_handler(func=lambda message:
    message.text and
    message.text.strip().split() and
    message.text.strip().split()[-1].rstrip('.,!').lower() == "нет"
)
def handle_no_word(message):
    if not message.text or not message.text.strip():
        return

    # Разбиваем текст на слова и берём последнее слово
    words = message.text.strip().split()
    last_word = words[-1].lower() if words else None
    # Отвечаем на сообщения с "нет" в конце
    bot_response_no = random.choice(bot_answer_no)

    # bot.reply_to(message, f"{random.choice(bot_answer_no)}")
    bot_reply_with_probability(message, bot_response_no, 0.40)


# 5.2. Обработчик слова "нэ"
@bot.message_handler(func=lambda message:
    message.text and
    message.text.strip().split() and
    message.text.strip().split()[-1].rstrip('.,!').lower() == "нэ"
)
def handle_no_word(message):
    if not message.text or not message.text.strip():
        return

    # Разбиваем текст на слова и берём последнее слово
    words = message.text.strip().split()
    last_word = words[-1].lower() if words else None
    # Отвечаем на сообщения с "нэ" в конце
    bot_response_no_ukr = random.choice(bot_answer_no_ukr)

    # bot.reply_to(message, f"{random.choice(bot_answer_no_ukr)}")
    bot_reply_with_probability(message, bot_response_no_ukr, 0.40)


# 5.3. Обработчик слова "да"
@bot.message_handler(func=lambda message:
    message.text and
    message.text.strip().split() and
    message.text.strip().rstrip('.,!?;:').lower().startswith('д') and
    all(c in 'да' for c in message.text.strip().rstrip('.,!?;:').lower()) and
    len(message.text.strip().rstrip('.,!?;:')) >= 2
)
def handle_yes_word(message):
    # Дополнительная проверка
    clean_text = message.text.strip().rstrip('.,!?;:').lower()
    bot_response_yes = random.choice(bot_answer_yes)

    # Проверяем что это вариация "да" (начинается на "д", остальное - "а")
    if (clean_text.startswith('д') and
            all(char == 'а' for char in clean_text[1:])):
        # bot.reply_to(message, f"{random.choice(bot_answer_yes)}")
        bot_reply_with_probability(message, bot_response_yes, 0.50)

# 5.4. Обработчик слова "ага"
@bot.message_handler(func=lambda message:
    message.text and
    message.text.strip().split() and
    message.text.strip().split()[-1].rstrip('.,!?:;').lower() == "ага"
)
def handle_aga_word(message):
    if not message.text or not message.text.strip():
        return

    # Разбиваем текст на слова и берём последнее слово
    words = message.text.strip().split()
    last_word = words[-1].lower() if words else None
    bot_response_aga = random.choice(bot_answer_aga)

    # Отвечаем на сообщения с "ага" в конце
    # bot.reply_to(message, f"{random.choice(bot_answer_aga)}")
    bot_reply_with_probability(message, bot_response_aga, 0.90)






# Добавляем в обработчик сообщений (только сбор пользователей)
@bot.message_handler(content_types=['text'])
def handle_message(message):
    # Собираем пользователя
    auto_collect_users(message)





#--------------------------------------------------------------------------------------------

# Функция для получения случайного анекдота
def get_random_joke():
    try:
        # Источник 1: anekdot.ru (парсинг)
        url = "https://www.anekdot.ru/random/anekdot/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        jokes = soup.find_all('div', class_='text')

        if jokes:
            # Фильтруем только хорошие анекдоты
            clean_jokes = []
            for joke in jokes:
                joke_text = joke.get_text().strip()
                if len(joke_text) > 20 and "©" not in joke_text:  # Отсеиваем короткие и с копирайтами
                    clean_jokes.append(joke_text)

            if clean_jokes:
                return random.choice(clean_jokes)

        # Если не получилось с парсингом, используем запасной вариант
        return get_backup_joke()

    except Exception as e:
        print(f"Ошибка при получении анекдота: {e}")
        return get_backup_joke()


# Запасная функция с локальной базой анекдотов
def get_backup_joke():
    backup_jokes = [
        "Программист звонит в библиотеку:\n- Здравствуйте, Камю «Посторонний» есть?\n- Да, но он для программистов не подходит.\n- Почему?\n- Там нужно вводить капчу.",
        "Приходит программист к психологу:\n- Доктор, у меня проблема: я всё время думаю, что я - собака.\n- Садитесь, пожалуйста, на диван.\n- Нельзя, я с дивана лаю.",
        "Сидят два программиста, один другому:\n- Слушай, а ведь женщины - это как операционная система:\nстоит дорого, много глюков, а документации всё равно нет.",
        "Объявление: \"Требуется программист. Зарплата от 100к. Опыт работы от 3 лет. Знание 15 языков программирования. Возраст до 25 лет.\"",
        "Почему программисты так плохо водят машину?\nПотому что во время обучения они всё время смотрят не на дорогу, а на компилятор.",
        "- Дорогой, купи хлеба!\n- OK\n- И если яйца есть, купи десяток.\nВечером программист возвращается с десятью батонами.",
        "Программист рассказывает жене:\n- Представляешь, нашёл сегодня баг, который искал полгода!\n- И что, починил?\n- Нет, перезапустил компьютер и он исчез.\n- Ну и к чему тогда вся эта радость?\n- Баг-то воспроизводимый был!",
        "Стоят два программиста, смотрят на закат.\nПервый: \"Какая красивая картина...\"\nВторой: \"Неоптимально rendered. Слишком много полигонов.\"",
        "Почему программисты путают Хэллоуин и Рождество?\nПотому что Oct 31 == Dec 25.",
        "Программист приходит в бар и заказывает 1.5 литра пива.\nБармен: \"Это что, на компанию?\"\nПрограммист: \"Нет, на вечеринку. 1.5 литра = 1 литр + 500 мл.\""
    ]
    return random.choice(backup_jokes)

#--------------------------------------------------------------------------------------------

# bot.infinity_polling(timeout=10, long_polling_timeout=5)
bot.polling(none_stop=True)