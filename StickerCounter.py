import sqlite3
import os
from datetime import datetime

class StickerCounter:
    def __init__(self, db_path='sticker_counter.sqlite'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        '''Инициализация базы данных для счётчика стикеров'''
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS sticker_stats (
                user_id INTEGER,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                chat_id INTEGER,
                sticker_count INTEGER DEFAULT 0,
                last_sticker_date TEXT,
                PRIMARY KEY (user_id, chat_id)
            )
                           ''')

            conn.commit()
            conn.close()
            print('✅ База данных для счётчика стикеров создана')

        except Exception as e:
            print(f"❌ Ошибка при создании базы стикеров: {e}")

    def add_sticker(self, user_id, username, first_name, last_name, chat_id, sticker_id=None):
        """Добавляет +1 к счётчику пользователя"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            current_time = datetime.now().isoformat()

            # Проверим, существует ли пользователь
            cursor.execute('''
            SELECT sticker_count FROM sticker_stats 
            WHERE user_id = ? AND chat_id = ?
            ''',  (user_id, chat_id))

            result = cursor.fetchone()

            if result:
                # Обновляем существующего пользователя
                new_count = 1
                cursor.execute('''
                UPDATE sticker_stats 
                SET sticker_count = ?, last_sticker_date = ?, username = ?, first_name = ?, last_name = ?
                WHERE user_id = ? AND chat_id = ?
                ''', (new_count, current_time, username, first_name, last_name, user_id, chat_id))
            else:
                # Добавляем нового пользователя
                new_count = 1
                cursor.execute('''
                INSERT INTO sticker_stats 
                (user_id, username, first_name, last_name, chat_id, sticker_count, last_sticker_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, username, first_name, last_name, chat_id, new_count, current_time))

            conn.commit()
            conn.close()

            print(f"✅ Стикер добавлен: {username or first_name} - {new_count} шт.")
            return new_count

        except Exception as e:
            print(f"❌ Ошибка при добавлении стикера: {e}")
            return None

    def get_sticker_count(self, user_id, chat_id):
        # Получает количество стикеров пользователя
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''    
            SELECT sticker_count FROM sticker_stats 
            WHERE user_id = ? AND chat_id = ?
            ''', (user_id, chat_id))

            result = cursor.fetchone()
            conn.close()

            return result[0] if result else 0

        except Exception as e:
            print(f"❌ Ошибка при получении счета стикеров: {e}")
            return 0

    def get_top_sticker_users(self, chat_id, limit = 10):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
            SELECT username, first_name, last_name, sticker_count 
            FROM sticker_stats 
            WHERE chat_id = ?
            ORDER BY sticker_count DESC 
            LIMIT ?
            ''', (chat_id, limit))

            users = cursor.fetchall()
            conn.close()
            return users

        except Exception as e:
            print(f"❌ Ошибка при получении топа стикеров: {e}")
            return []

    def get_total_stickers_in_chat(self):
        "Получает общее количество стикеров в чате"
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
            SELECT SUM(sticker_count) FROM sticker_stats 
            WHERE chat_id = ?
            ''', (chat_id,))

            result = cursor.fetchone()
            conn.close()

            return result[0] if result [0] else 0

        except Exception as e:
            print(f"❌ Ошибка при получении общего количества стикеров: {e}")
            return 0

    def get_stickers_stats(self, chat_id):
        """Получает полную статистику по стикерам пользователя"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            с = cursor.execute('''
            SELECT sticker_count, last_sticker_date 
            FROM sticker_stats 
            WHERE user_id = ? AND chat_id = ?
            ''', (user_id, chat_id))

            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    'sticker_count': result[0],
                    'last_sticker_date': result[1],
                }
            else:
                return {'sticker_count': 0, 'last_sticker_date': None}

        except Exception as e:
            print(f"❌ Ошибка при получении статистики стикеров: {e}")
            return {'sticker_count': 0, 'last_sticker_date': None}
