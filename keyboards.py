from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from manage_data import audio_formats, SELECT_FORMAT, SELECT_LANGUAGE

buttons = []

for audio_format in audio_formats:
    buttons.append(InlineKeyboardButton(audio_format, callback_data=f"{SELECT_FORMAT}.{audio_format}"))


def formats_keyboard():
    return InlineKeyboardMarkup([buttons])


def lang_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("English", callback_data=f"{SELECT_LANGUAGE}.en"),
            InlineKeyboardButton("Русский", callback_data=f"{SELECT_LANGUAGE}.ru")
        ]
    ])


def mp3_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("MP3", callback_data=f"{SELECT_FORMAT}.mp3")
        ]
    ])
