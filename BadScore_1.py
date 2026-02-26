import sqlite3
from datetime import datetime

from config import BAD_SCORE_DB_PATH


# Инициализация базы данных для счётчика матов
def init_bad_score_db(db_path: str = BAD_SCORE_DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_scores (
            user_id INTEGER,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            chat_id INTEGER,
            register_date TEXT,
            score INTEGER DEFAULT 0,
            last_updated TEXT,
            PRIMARY KEY (user_id, chat_id)
        )
        ''')

        conn.commit()
        conn.close()
        print("✅ База данных счётчика матов создана")

    except Exception as e:
        print(f"❌ Ошибка при создании базы счётчика: {e}")


# Функция для увеличения счёта матов
def increase_bad_score(user_id, username, first_name, last_name, chat_id, db_path: str = BAD_SCORE_DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        current_time = datetime.now().isoformat()

        # Проверяем существует ли пользователь
        cursor.execute('SELECT score FROM user_scores WHERE user_id = ? AND chat_id = ?',
                       (user_id, chat_id))
        result = cursor.fetchone()

        if result:
            # Обновляем существующего пользователя
            new_score = result[0] + 1
            cursor.execute('''
            UPDATE user_scores 
            SET score = ?, last_updated = ?, username = ?, first_name = ?, last_name = ?
            WHERE user_id = ? AND chat_id = ?
            ''', (new_score, current_time, username, first_name, last_name, user_id, chat_id))
        else:
            # Добавляем нового пользователя
            new_score = 1
            cursor.execute('''
            INSERT INTO user_scores 
            (user_id, username, first_name, last_name, chat_id, register_date, score, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, chat_id, current_time, new_score, current_time))

        conn.commit()
        conn.close()
        return new_score

    except Exception as e:
        print(f"❌ Ошибка при обновлении счёта: {e}")
        return None


# Функция для получения текущего счёта
def get_bad_score(user_id, chat_id, db_path: str = BAD_SCORE_DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT score FROM user_scores WHERE user_id = ? AND chat_id = ?',
                       (user_id, chat_id))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else 0

    except Exception as e:
        print(f"❌ Ошибка при получении счёта: {e}")
        return 0


# Функция для получения топа нарушителей
def get_top_bad_scores(chat_id, limit=10, db_path: str = BAD_SCORE_DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT username, first_name, last_name, score 
        FROM user_scores 
        WHERE chat_id = ?
        ORDER BY score DESC 
        LIMIT ?
        ''', (chat_id, limit))

        users = cursor.fetchall()
        conn.close()
        return users

    except Exception as e:
        print(f"❌ Ошибка при получении топа: {e}")
        return []


# Инициализируем базу при импорте
init_bad_score_db()


