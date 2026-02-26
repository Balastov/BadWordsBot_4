import logging
import random

import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def get_random_joke() -> str:
    """
    Возвращает случайный анекдот.

    Сначала пытаемся спарсить anekdot.ru, при ошибке используем локальный список.
    """
    try:
        url = "https://www.anekdot.ru/random/anekdot/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        jokes = soup.find_all("div", class_="text")

        clean_jokes = []
        for joke in jokes:
            joke_text = joke.get_text().strip()
            if len(joke_text) > 20 and "©" not in joke_text:
                clean_jokes.append(joke_text)

        if clean_jokes:
            return random.choice(clean_jokes)

        return get_backup_joke()

    except Exception as e:
        logger.error("Ошибка при получении анекдота: %s", e)
        return get_backup_joke()


def get_backup_joke() -> str:
    """Локальный запасной список анекдотов."""
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
        "Программист приходит в бар и заказывает 1.5 литра пива.\nБармен: \"Это что, на компанию?\"\nПрограммист: \"Нет, на вечеринку. 1.5 литра = 1 литр + 500 мл.\"",
    ]
    return random.choice(backup_jokes)


__all__ = ["get_random_joke", "get_backup_joke"]

