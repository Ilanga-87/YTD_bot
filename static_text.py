about_bot = """
The bot that will help you to download audio files from YouTube videos
"""

description = """
This bot downloads audio files from YouTube videos. 
To start downloading input youtube url.
To select file format press the button.
Please note that Telegram does not allow bots to send files larger than 50 MB. 
Too large files need to be compressed. Thank you for your understanding.

If you want to download file more than 50 MB, you can visit https://mp3-from-youtube.com/.
If you face any trouble with bot or site, you can write a bug report here: https://t.me/yttab_discussion

"""

messages = {
    "en": {
        "welcome_text": """
        Hi! I will download for you sound from YouTube videos in any of next format: mp3, wav, flac, m4a.
To start you should input youtube url.
Than select necessary format and enjoy!
If you need more information please look at /help.

Please note that Telegram does not allow sending files larger than 50 MB to bots. 
Therefore, if the file is very large, it will need to be compressed. Thank you for your understanding.
        """,
        "select_lang_text": """
        Select language: 
        """,
        "selected_lang_text": """
        You selected English. You can change it by /start command.
        """,
        "wait_text": """
        Please wait a moment. It can take more time if selected file is big or if YouTube servers are too busy.
        """,
        "help_text": """
        You can start download just by pasting YouTube url. Then you should select audio format for your file.
If you want to download file more than 50 MB, you can visit https://mp3-from-youtube.com/.
If you face any trouble with bot or site, you can write a bug report here: https://t.me/yttab_discussion
        """,
        "undefined_command_text": """
        Sorry, I didn't understand that command. May be /help can be useful for you.
        """,
        "ready_notification_text": """
        It's ready ⬇️⬇️⬇️
        """,
        "select_format_text": """
        Select preferred audio format to download: 
        """,
        "audio_name_text": """
        You want to download audio 
        """,
        "check_url_text": """
        Please check copied URL.
        """,
        "wrong_url_text": """
        Sorry, something went wrong when sending the file to the chat. 
We will definitely figure out what the problem is. 
In the meantime, you can send another link. 
        """,
        "you_tube_error_text": """
        Sorry, the YouTube server is not responding. We hope it's temporary, please try again later.
        """,
        "file_too_long_text": """
        Sorry, the file {} is too long: {}. Bot cannot convert it to size allowed Telegram (50M).
        """,
        "need_compress_text": """
        The file {} is too big to download it in uncompressed formats. Recommend to download it as mp3.
        """
    },
    "ru": {
        "welcome_text": """
        Приветствую! Здесь вы можете скачать аудио с YouTube в любом из этих форматов: mp3, wav, flac, m4a.
Чтобы начать, просто отправьте боту ссылку. Потом выберите формат и немного подождите.
Если вам нужна помощь, в любой момент отправьте боту команду /help.

Обратите внимание, что Телеграм не позволяет отправлять боту файлы более 50 м. 
Поэтому, если файл очень большой, его придется сжать. Благодарим за понимание.
        """,
        "select_lang_text": """
        Выберите язык: 
        """,
        "selected_lang_text": """
        Вы выбрали русский. Вы можете изменить язык, набрав команду /start.
        """,
        "wait_text": """
        Ваш запрос обрабатывается... Это может занять некоторое время, если файл большой или сервера загружены.
        """,
        "help_text": """
        Просто отправьте боту ссылку на видео в YouTube и выберите нужный аудио формат.
Если вы хотите скачать файл больше 50 MB, вы можете воспользоваться сайтом https://mp3-from-youtube.com/.
Если вы столкнулись с какими-то проблемами, пишите: https://t.me/yttab_discussion
        """,
        "undefined_command_text": """
        Извините, я не знаю такой команды.
        """,
        "ready_notification_text": """
        Готово ⬇️⬇️⬇️
        """,
        "select_format_text": """
        Выберите формат для вашего аудио файла перед скачиванием: 
        """,
        "audio_name_text": """
        Вы выбрали файл 
        """,
        "check_url_text": """
        Пожалуйста, вставьте правильную ссылку на YouTube.
        """,
        "wrong_url_text": """
Извините, что-то пошло не так при отправке файла в чат. Мы обязательно разберемся, в чем проблема. 
Пока вы можете отправить другую ссылку. 
        """,
        "you_tube_error_text": """
        Извините, сервер youtube не отвечает. Надеемся, это ненадолго, попробуйте снова чуть позже. 
        """,
        "file_too_long_text": """
        Извините, выбранное видео {} слишком длинное: {}. Даже при сильном сжатии оно больше разрешенных Телеграм 50 мегабайт. 
        """,
        "need_compress_text": """
        Видео {} превышает лимиты Телеграм для отправки ботом при конвертации с несжимаемые форматы. Рекомендуется конвертация в mp3.
        """
    }
}

welcome_text = """
Hi! I will download for you sound from YouTube videos in any of next format: mp3, wav, flac, m4a.
To start you should input youtube url.
Than select necessary format and enjoy!
If you need more information please look at /help.
"""

wait_text = """
Please wait a moment. It can take more time if selected file is big or if YouTube servers are too busy.
"""

help_text = """
You can start download just by pasting YouTube url. Then you should select audio format for your file.
"""

undefined_command_text = """
Sorry, I didn't understand that command. May be /help can be useful for you.
"""
