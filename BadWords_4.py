# 7856651931:AAGkiOiF964M_AcjfCsheAHXXQ5dfC0rXB4
import random
# from datetime import datetime
import telebot
from bs4 import BeautifulSoup
import requests
import sqlite3
from DailyEvents import DailyEvents
# import os

# import random

# from telegram._utils import markup

bot = telebot.TeleBot('8384870189:AAEViu4Ee_0jD6-SU7F6TQMHIJCLUyT-SI4')
daily_events = DailyEvents(bot)

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
                    "Пойди, книжку почитай.", "Я есть Грут!"
                        ]

bot_answer_no = ["Пидора ответ", "Хипстора планшет", "Гомогея ответ", "Голый пистолет", "В Турцию билет",
                 "Сам знаешь, чей ответ", "Розовый берет", "Скользкий парапет", "Чайковского балет",
                 "Группа Nazareth", "От Дилдоджона привет"
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
    "перестрахуй", "перестрахование"
]

bad_words = ["хуй", "хyй", "xyй", "хуёвый", "хуевый", "хуёвые", "хуевая", "хуёвая", "хуя", "хуета", "х у й", "п и з д а",
    "хуевые", "хуёвые", "нахуевертить", "хуишко", "хууй", "хуууй", "хууууй", "хуууууй", "хууууууй", "хуле",
    "ахуел", "хуила",
    "пизда", "песда", "песдец", "пиздец", "пиздатый", "пиздатая", "пиздюлина", "пизды",
    "пиздюлины", "пиздюлину", "пиздюлин", "пиздюлей", "пиздюк", "песдюк", "пизду", "пиздуй", "пиздуешь",
    "пзду", "опездал", "опездол", "шопиздец",
    "ебанутый", "ебанашка", "ебан", "йбал", "ебобаный", "ебобаных", "ебобаная", "уебище",
    "ебанашки", "ебанашке", "ебанашку", "ебанутая", "ебанутой", "ебанутые", "ебашит",
    "наебенился", "ебашь", "выеби",
    "ебанутую", "ебанутого", "йобаный", "ебать", "ебу", "ебал", "наебовертить", "долбоёб", "долбоеб",
    "долбаеб", "разъёб", "наёбан", "наебан", "е б а т ь", "еблан", "сьебал",
    "охуенный", "охуенная", "хуила", "охуел", "охуеть", "ахуенно",
    "охуенное", "охуенные", "хуесос", "хуесосы", "ахуеть", "охуеть", "хер", "херовый", "херовая", "херовые",
    "бля", "блядь", "блять", "блядина", "блядин", "блядину", "пидор", "пидар", "пидорас", "пидарас", "педрила",
    "пидрила", "пидр", "ебальник", "ебало", "ёбла", "гандон", "гондон", "шлюха", "залупа",
    "манда", "членосос",
    "педик", "говно", "говноед",
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


# Единая функция главного меню
def show_main_menu(chat_id, message_text="🤖 Главное меню"):
    """Показывает главное меню"""
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton('Admin')
    btn2 = telebot.types.KeyboardButton('Играть в кампуктер')
    btn3 = telebot.types.KeyboardButton('Start Events')
    btn4 = telebot.types.KeyboardButton('Перепись матершинников')
    btn5 = telebot.types.KeyboardButton('Шутка за 300')

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




@bot.message_handler(func=lambda message: message.text == 'Играть в кампуктер')
def test_menu(message):
    # Создаём выпадающее меню для "Играть в кампуктер"
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    # Добавляем кнопки подменю "Играть в кампуктер"
    btn1 = telebot.types.KeyboardButton('Paladins')
    btn2 = telebot.types.KeyboardButton('Supreme Commander')
    btn3 = telebot.types.KeyboardButton('Гоночки')
    btn4 = telebot.types.KeyboardButton('Satisfactory')
    btn_back = telebot.types.KeyboardButton('🔙 Назад')

    markup.add(btn1, btn2, btn3, btn4, btn_back)

    # Отправляем сообщение с подменю
    bot.send_message(message.chat.id, "Во что ты хочешь поиграть с товарищами?", reply_markup=markup)

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

@bot.message_handler(func=lambda message: message.text == 'Перепись матершинников')
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
    bot.send_message(message.chat.id, "😏 Ок, я понял, тебе захотелось публичных унижений.\nЛадно, "
                                      "давай поищем тех, кто тоже не против лишиться последних капель дофамина "
                                      "в организме.\n@mr_clown_baban @Balastov @utka_uwu @ongad @Lobok000 "
                                      "@zloifikyc @sheynnette, пробудитесь!"
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
    user = message.from_user

    # Увеличиваем счёт матов
    new_score = increase_bad_score(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        chat_id=message.chat.id
    )
    # Отправляем ответ

    username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    if new_score is not None:
        bot.reply_to(message, f"{username}, {random.choice(bot_answer_bad_words)}\n"
                                  f"У тебя теперь {new_score} баллов.")
    else:
        # Если произошла ошибка, используем альтернативный ответ
        bot.reply_to(message, f"{username}, Много болтаешь..")



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
    bot.reply_to(message, f"{random.choice(bot_answer_no)}")


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
    bot.reply_to(message, f"{random.choice(bot_answer_no_ukr)}")

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

    # Проверяем что это вариация "да" (начинается на "д", остальное - "а")
    if (clean_text.startswith('д') and
            all(char == 'а' for char in clean_text[1:])):
        bot.reply_to(message, f"{random.choice(bot_answer_yes)}")

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
    # Отвечаем на сообщения с "ага" в конце
    bot.reply_to(message, f"{random.choice(bot_answer_aga)}")






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