import logging
import random

from bot_app import bot
from constants import (
    ballov_nemalo,
    bot_answer_aga,
    bot_answer_no,
    bot_answer_no_ukr,
    bot_answer_yes,
    bot_answer_bad_words,
    bot_replay_answer_bad_words,
)
from services.reply_service import (
    REPLY_PROB_AGA,
    REPLY_PROB_BAD_WORDS,
    REPLY_PROB_NO,
    REPLY_PROB_NO_UKR,
    REPLY_PROB_YES,
    bot_reply_with_probability,
    contains_bad_words,
)
from services.stats_service import increment_bad_score


logger = logging.getLogger(__name__)


def _get_last_clean_word(text: str) -> str | None:
    """Возвращает последнее слово без знаков препинания, в нижнем регистре."""
    if not text or not text.strip():
        return None
    words = text.strip().split()
    if not words:
        return None
    return words[-1].rstrip(".,!?:;").lower()


def _ends_with_word(target: str):
    """Фабрика предиката для message_handler по последнему слову."""

    def _checker(message) -> bool:
        if not message or not getattr(message, "text", None):
            return False
        return _get_last_clean_word(message.text) == target

    return _checker


@bot.message_handler(func=lambda message: contains_bad_words(message.text))
def handle_bad_words(message) -> None:
    """Обработчик сообщений с матом."""
    try:
        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name

        new_score = increment_bad_score(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            chat_id=message.chat.id,
        )

        is_reply_to_bot = (
            message.reply_to_message
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.id == bot.get_me().id
        )

        phrases = (
            bot_replay_answer_bad_words
            if is_reply_to_bot
            else bot_answer_bad_words
        )

        score_text = (
            f"{random.choice(ballov_nemalo)} {new_score}!"
            if new_score is not None
            else ""
        )
        bot_response = f"{username}, {random.choice(phrases)}\n{score_text}".strip()

        bot_reply_with_probability(
            message, bot_response, probability=REPLY_PROB_BAD_WORDS
        )
    except Exception as e:
        logger.error("❌ Ошибка в обработчике матов: %s", e)


@bot.message_handler(func=_ends_with_word("нет"))
def handle_no_word(message) -> None:
    """Обработчик слова 'нет' в конце сообщения."""
    if not message.text or not message.text.strip():
        return

    bot_response_no = random.choice(bot_answer_no)
    bot_reply_with_probability(
        message, bot_response_no, probability=REPLY_PROB_NO
    )


@bot.message_handler(func=_ends_with_word("нэ"))
def handle_no_ukr_word(message) -> None:
    """Обработчик слова 'нэ' в конце сообщения."""
    if not message.text or not message.text.strip():
        return

    bot_response_no_ukr = random.choice(bot_answer_no_ukr)
    bot_reply_with_probability(
        message, bot_response_no_ukr, probability=REPLY_PROB_NO_UKR
    )


@bot.message_handler(
    func=lambda message: (
        message.text
        and message.text.strip().split()
        and message.text.strip()
        .rstrip(".,!?;:")
        .lower()
        .startswith("д")
        and all(
            c in "да"
            for c in message.text.strip()
            .rstrip(".,!?;:")
            .lower()
        )
        and len(
            message.text.strip().rstrip(".,!?;:")
        )
        >= 2
    )
)
def handle_yes_word(message) -> None:
    """Обработчик вариаций 'дааааа'."""
    clean_text = message.text.strip().rstrip(".,!?;:").lower()
    bot_response_yes = random.choice(bot_answer_yes)

    if clean_text.startswith("д") and all(char == "а" for char in clean_text[1:]):
        bot_reply_with_probability(
            message, bot_response_yes, probability=REPLY_PROB_YES
        )


@bot.message_handler(func=_ends_with_word("ага"))
def handle_aga_word(message) -> None:
    """Обработчик слова 'ага' в конце сообщения."""
    if not message.text or not message.text.strip():
        return

    bot_response_aga = random.choice(bot_answer_aga)
    bot_reply_with_probability(
        message, bot_response_aga, probability=REPLY_PROB_AGA
    )

