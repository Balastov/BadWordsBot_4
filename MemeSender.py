from tokenize import group

import requests
import random
import threading
import time
from datetime import datetime
import os



class MemeSender:
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.meme_sources = [
            self._get_meme_from_vk,
            self._get_meme_from_pikabu,
            self._get_meme_from_telegram_channels,
            self._get_backup_russian_meme
        ]

