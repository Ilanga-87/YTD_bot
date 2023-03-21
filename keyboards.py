from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from manage_data import audio_formats, SELECT_FORMAT

buttons = []

for audio_format in audio_formats:
    buttons.append(InlineKeyboardButton(audio_format, callback_data=f"{SELECT_FORMAT}.{audio_format}"))


def formats_keyboard():
    return InlineKeyboardMarkup([buttons])
