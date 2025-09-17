import requests
import random
from datetime import datetime
import threading
import time
from bs4 import BeautifulSoup
import json


class DailyEvents:
    def __init__(self, bot):
        self.bot = bot
        self.running = False

    def get_daily_events(self):
        """Получает праздники и события на сегодня из интернета"""
        try:
            today = datetime.now()

            # Пробуем разные источники по очереди
            events = self._get_events_from_wikipedia(today)
            if events:
                return events

            events = self._get_events_from_calend_ru(today)
            if events:
                return events

            events = self._get_events_from_historical_events_api()
            if events:
                return events

            # Если все API недоступны
            return self._get_backup_events()

        except Exception as e:
            print(f"❌ Ошибка при получении событий: {e}")
            return self._get_backup_events()

    @staticmethod
    def _get_events_from_wikipedia(today):
        """Получает события из Википедии"""
        try:
            url = f"https://ru.wikipedia.org/wiki/{today.strftime('%d_%B')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            events = []

            # Ищем раздел "События"
            events_section = soup.find('span', {'id': 'События'})
            if events_section:
                events_list = events_section.find_next('ul')
                if events_list:
                    for item in events_list.find_all('li', limit=5):
                        event_text = item.get_text().strip()
                        if event_text and len(event_text) > 10:
                            events.append(event_text)

            return events if events else None

        except:
            return None

    @staticmethod
    def _get_events_from_calend_ru(today):
        """Получает праздники с calend.ru"""
        try:
            url = f"https://www.calend.ru/day/{today.strftime('%Y-%m-%d')}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            events = []

            # Ищем блоки с праздниками
            holiday_blocks = soup.find_all('div', class_='caption')
            for block in holiday_blocks[:5]:
                title = block.find('a')
                if title:
                    event_text = title.get_text().strip()
                    if event_text:
                        events.append(event_text)

            return events if events else None

        except:
            return None

    @staticmethod
    def _get_events_from_historical_events_api():
        """Получает исторические события из API"""
        try:
            # API исторических событий
            url = "https://api.api-ninjas.com/v1/historicalevents"
            headers = {'X-Api-Key': 'YOUR_API_KEY'}  # Можно оставить пустым для теста

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                events_data = response.json()
                events = []
                for event in events_data[:3]:
                    if 'event' in event:
                        events.append(event['event'])
                return events if events else None

        except:
            pass

        # Альтернативный источник - локальный файл с событиями
        # try:
        #     return self._get_events_from_local_file()
        # except:
        #     return None

    # @staticmethod
    # def _get_events_from_local_file():
    #     """Резервный источник событий из файла"""
    #     historical_events = [
    #         "1989 - Падение Берлинской стены",
    #         "1969 - Первая высадка человека на Луну (Аполлон-11)",
    #         "1945 - Окончание Второй мировой войны",
    #         "1991 - Распад Советского Союза",
    #         "1961 - Первый полет человека в космос (Юрий Гагарин)",
    #         "1917 - Октябрьская революция в России",
    #         "1812 - Отечественная война с Наполеоном",
    #         "1941 - Начало Великой Отечественной войны",
    #         "1957 - Запуск первого спутника Земли",
    #         "1986 - Авария на Чернобыльской АЭС",
    #         "2001 - Теракты 11 сентября в США",
    #         "1945 - Ядерная бомбардировка Хиросимы и Нагасаки",
    #         "1962 - Карибский кризис",
    #         "1980 - Летние Олимпийские игры в Москве",
    #         "1999 - Возвращение Косово под управление ООН"
    #     ]
    #     return [random.choice(historical_events)]

    @staticmethod
    def _get_backup_events():
        """Резервные события если ничего не найдено"""
        backup_events = [
            ["Сегодня отличный день чтобы сделать мир лучше!"],
            ["Помните: каждый день - это возможность для новых свершений!"],
            ["Сегодняшний день в истории: обычный день, который можно сделать особенным!"],
            ["Ничего особенного не произошло, но это повод создать свое собственное событие!"]
        ]
        return random.choice(backup_events)

    @staticmethod
    def format_message(events):
        """Форматирует сообщение с событиями"""
        today = datetime.now()
        message = f"📅 {today.strftime('%d.%m.%Y')}\n\n"

        if len(events) == 1:
            message += f"🎉 Сегодня: {events[0]}\n\n"
        else:
            message += "🎉 Сегодня:\n"
            for i, event in enumerate(events[:3], 1):  # Берем первые 3 события
                message += f"{i}. {event}\n"
            message += "\n"

        # message += "📜 Историческое событие дня:\n"
        # message += f"• {self._get_events_from_local_file()[0]}\n\n"
        message += "@utka_uwu Утка, с Днём Рождения! 👾"

        return message

    def send_daily_event(self, chat_id):
        """Отправляет ежедневное событие в чат"""
        try:
            events = self.get_daily_events()
            message = self.format_message(events)
            self.bot.send_message(chat_id, message)
            print(f"✅ Событие отправлено в чат {chat_id}")
        except Exception as e:
            print(f"❌ Ошибка отправки события: {e}")

    def start_daily_scheduler(self, chat_id, hour=8, minute=0):
        """Запускает ежедневную отправку в 8:00 по МСК"""

        def scheduler():
            while self.running:
                now = datetime.now()
                # Для московского времени (UTC+3)
                msk_hour = (now.hour + 3) % 24

                if msk_hour == hour and now.minute == minute:
                    self.send_daily_event(chat_id)
                    time.sleep(61)  # Ждем минуту чтобы не отправить повторно

                time.sleep(30)  # Проверяем каждые 30 секунд

        self.running = True
        thread = threading.Thread(target=scheduler)
        thread.daemon = True
        thread.start()
        print(f"✅ Ежедневный планировщик запущен для чата {chat_id}")

    def stop_scheduler(self):
        """Останавливает планировщик"""
        self.running = False


