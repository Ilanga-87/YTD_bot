from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from static_text import audio_formats

buttons = []

for audio_format in audio_formats:
    buttons.append(InlineKeyboardButton(audio_format, callback_data=audio_format))


def formats_keyboard():
    return InlineKeyboardMarkup([buttons])
