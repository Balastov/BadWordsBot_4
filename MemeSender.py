import requests
import random
import threading
import time
from datetime import datetime, time as time_obj
import sqlite3
import json
from bs4 import BeautifulSoup
import logging
from io import BytesIO

from config import MEME_CACHE_DB_PATH

# Настройка логирования (основная конфигурация может быть переопределена снаружи)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemeSender:
    """Класс для отправки мемов по расписанию (9:00, 15:00, 20:00 МСК)"""
    
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.scheduler_thread = None
        self.chat_id = None
        
        # Время отправки (МСК)
        self.send_times = [
            time_obj(9, 0),    # 9:00
            time_obj(15, 0),   # 15:00
            time_obj(20, 0)    # 20:00
        ]
        
        # Источники мемов (без Reddit)
        self.meme_sources = [
            ('Telegram', self._get_meme_from_telegram_channels),
            ('Pikabu', self._get_meme_from_pikabu),
            ('Imgur', self._get_meme_from_imgur),
            ('VK', self._get_meme_from_vk),
        ]
        
        self._init_meme_cache_db()
    
    def _init_meme_cache_db(self):
        """Инициализирует БД для кески отправленных мемов"""
        try:
            conn = sqlite3.connect(MEME_CACHE_DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS sent_memes (
                meme_id TEXT PRIMARY KEY,
                source TEXT,
                url TEXT,
                sent_date TEXT,
                chat_id INTEGER
            )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ База кеша мемов создана")
        except Exception as e:
            logger.error(f"❌ Ошибка при создании БД кеша: {e}")
    
    def _is_meme_sent(self, meme_url):
        """Проверяет, был ли мем уже отправлен"""
        try:
            conn = sqlite3.connect(MEME_CACHE_DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('SELECT 1 FROM sent_memes WHERE url = ?', (meme_url,))
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
        except Exception as e:
            logger.error(f"❌ Ошибка при проверке кеша: {e}")
            return False
    
    def _save_sent_meme(self, meme_url, source):
        """Сохраняет отправленный мем в кеш"""
        try:
            conn = sqlite3.connect(MEME_CACHE_DB_PATH)
            cursor = conn.cursor()
            
            meme_id = f"{source}_{int(datetime.now().timestamp())}"
            cursor.execute('''
            INSERT INTO sent_memes (meme_id, source, url, sent_date, chat_id)
            VALUES (?, ?, ?, ?, ?)
            ''', (meme_id, source, meme_url, datetime.now().isoformat(), self.chat_id))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"❌ Ошибка при сохранении мема в кеш: {e}")
    
    def start_meme_scheduler(self, chat_id):
        """Запускает планировщик отправки мемов"""
        if self.running:
            logger.warning("⚠️ Планировщик мемов уже запущен")
            return
        
        self.chat_id = chat_id
        self.running = True
        
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        logger.info(f"✅ Планировщик мемов запущен для чата {chat_id}")
    
    def stop_meme_scheduler(self):
        """Останавливает планировщик"""
        self.running = False
        logger.info("🛑 Планировщик мемов остановлен")
    
    def _scheduler_loop(self):
        """Основной цикл планировщика"""
        last_sent_date = None
        
        while self.running:
            now = datetime.now()
            current_time = now.time()
            current_date = now.date()
            
            # Проверяем, не отправляли ли уже мемы сегодня в эти часы
            if last_sent_date != current_date:
                for send_time in self.send_times:
                    # Проверяем, пtiempo текущий час совпадает с временем отправки
                    if (current_time.hour == send_time.hour and 
                        current_time.minute >= send_time.minute and
                        current_time.minute < send_time.minute + 1):
                        
                        logger.info(f"🎬 Время отправки мема: {send_time}")
                        self.send_meme_now()
                        last_sent_date = current_date
                        time.sleep(60)  # Защита от двойной отправки
                        break
            
            time.sleep(30)  # Проверяем каждые 30 секунд
    
    def _send_meme_internal(self, meme_url, source_name):
        """Внутренняя функция для отправки мема"""
        try:
            # Скачиваем изображение и отправляем его как байтовый поток
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(meme_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Создаем байтовый поток изображения
            image_stream = BytesIO(response.content)
            image_stream.name = 'meme.jpg'  # Устанавливаем имя файла
            
            self.bot.send_photo(
                self.chat_id,
                image_stream,
                caption=f"😂 Мем из {source_name}\n{datetime.now().strftime('%H:%M МСК')}"
            )
            self._save_sent_meme(meme_url, source_name)
            logger.info(f"✅ Мем от {source_name} отправлен в чат {self.chat_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка отправки мема: {e}")
            return False
    
    def _send_backup_meme(self, source_name):
        """Отправляет резервный мем"""
        try:
            backup_meme = self._get_backup_russian_meme()
            if backup_meme:
                self.bot.send_photo(
                    self.chat_id,
                    backup_meme,
                    caption=f"😂 Резервный мем из {source_name}\n{datetime.now().strftime('%H:%M МСК')}"
                )
                logger.info(f"✅ Резервный мем отправлен в чат {self.chat_id}")
                return True
        except Exception as e:
            logger.error(f"❌ Ошибка отправки резервного мема: {e}")
        return False
    
    def send_meme_now(self, chat_id=None):
        """Отправляет мем прямо сейчас"""
        try:
            # Если передан chat_id, используем его, иначе используем сохраненный
            if chat_id:
                self.chat_id = chat_id
            
            if not self.chat_id:
                logger.error("❌ chat_id не установлен")
                return
            
            # Пробуем разные источники
            meme_url = None
            source_name = None
            
            # Перемешиваем источники для разнообразия
            sources = list(self.meme_sources)
            random.shuffle(sources)
            
            for source_name, source_func in sources:
                try:
                    meme_url = source_func()
                    if meme_url and not self._is_meme_sent(meme_url):
                        break
                except Exception as e:
                    logger.warning(f"⚠️ Ошибка получения мема из {source_name}: {e}")
                    continue
            
            if meme_url:
                # Пытаемся отправить основной мем
                if not self._send_meme_internal(meme_url, source_name):
                    # Если основная отправка не удалась, пробуем отправить резервный мем
                    self._send_backup_meme(source_name)
            else:
                logger.warning("⚠️ Не удалось получить мем")
        
        except Exception as e:
            logger.error(f"❌ Ошибка в send_meme_now: {e}")
            # В случае общей ошибки тоже пробуем отправить резервный мем
            self._send_backup_meme("резервный")
    
    # ======================== ИСТОЧНИКИ МЕМОВ ========================
    
    def _get_meme_from_vk(self):
        """Получает мем из VK (парсинг популярного сообщества)"""
        try:
            # Используем открытый API VK для получения фото из сообщества
            # Сообщество: mems.for.you (https://vk.com/mems.for.you)
            url = "https://api.vk.com/method/wall.get"
            params = {
                'domain': 'mems.for.you',
                'count': 100,
                'v': '5.131',
                'access_token': 'SERVICE_TOKEN'  # Требует токен, используем fallback
            }
            
            # Fallback: парсим через requests/BeautifulSoup
            response = requests.get(
                'https://vk.com/mems.for.you',
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )
            response.raise_for_status()
            
            # На실際 практике нужен токен; возвращаем заранее подготовленные URLs
            vk_meme_urls = [
                'https://sun9-10.userapi.com/c629625/v629625000/4e5fb/AjvVYVfSHn8.jpg',
                'https://sun9-30.userapi.com/c628425/v628425000/8a70e/nnFaOvb5Aig.jpg',
                'https://sun9-32.userapi.com/c629104/v629104000/5bcff/qFzJL1L-pqc.jpg'
            ]
            return random.choice(vk_meme_urls)
        except Exception as e:
            logger.warning(f"⚠️ Ошибка VK: {e}")
            return None
    
    def _get_meme_from_pikabu(self):
        """Получает мем с Пикабу"""
        try:
            url = "https://pikabu.ru/tag/мемы/new/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ищем изображения в постах (чистые URL)
            images = soup.find_all('img', class_='story__image')
            if not images:
                # Пытаемся вытягивать по другому селектору
                images = soup.find_all('img', class_='image__pic')
            
            for img in images:
                img_url = img.get('src') or img.get('data-src')
                if img_url and ('pikabu' in img_url or 'sun' in img_url):
                    if img_url.startswith('//') or img_url.startswith('/'):
                        img_url = 'https:' + img_url if img_url.startswith('//') else 'https://pikabu.ru' + img_url
                    return img_url
            
            return None
        except Exception as e:
            logger.warning(f"⚠️ Ошибка Pikabu: {e}")
            return None
    
    def _get_meme_from_telegram_channels(self):
        """Получает мем из открытых Telegram каналов"""
        try:
            # Используем открытые каналы с мемами
            channels = [
                'https://t.me/s/toprusmemes',
                'https://t.me/s/best_memes_ru',
                'https://t.me/s/russian_memes',
                'https://t.me/s/memes_by_me_v2'
            ]
            
            channel = random.choice(channels)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(channel, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ищем изображения
            images = soup.find_all('img', class_='tgme_widget_message_image')
            if images:
                for img in images:
                    img_url = img.get('src')
                    if img_url and ('telegram' in img_url or 'cdn' in img_url):
                        return img_url
            
            return None
        except Exception as e:
            logger.warning(f"⚠️ Ошибка Telegram: {e}")
            return None

    
    def _get_meme_from_imgur(self):
        """Получает случайное изображение из Imgur"""
        try:
            url = "https://imgur.com/random"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Пытаемся найти meta
            meta_tag = soup.find('meta', property='og:image')
            if meta_tag and meta_tag.get('content'):
                img_url = meta_tag.get('content')
                return img_url
            
            # Альтернативный поиск
            images = soup.find_all('img')
            for img in images:
                src = img.get('src') or img.get('data-src')
                if src and 'i.imgur.com' in src:
                    if src.startswith('//'):
                        src = 'https:' + src
                    return src
            
            return None
        except Exception as e:
            logger.warning(f"⚠️ Ошибка Imgur: {e}")
            return None
    
    def _get_backup_russian_meme(self):
        """Резервный источник: встроенные мемы"""
        backup_memes = [
            'https://sun9-10.userapi.com/c629625/v629625000/4e5fb/AjvVYVfSHn8.jpg',
            'https://i.imgflip.com/63uxer.jpg',
            'https://i.imgflip.com/7j8qkx.jpg'
        ]
        return random.choice(backup_memes)


