import requests
import random
import threading
import time
from datetime import datetime
import sqlite3
from bs4 import BeautifulSoup

from BadWords_4 import bot


class QuestionsSender:
    def __init__(self):
        self.bot = bot
        self.running = False

    def random_user_from_db(self, chat_id):
        """Получаем случайного пользователя из базы1"""
        try:
            conn = sqlite3.connect('users_database.sqlite')
            cursor = conn.cursor()

            cursor.execute('''
            SELECT username, first_name, last_name
            FROM chat_users
            WHERE chat_id = ? AND username IS NOT NULL''', (chat_id,))
