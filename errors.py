import yt_dlp

import manage_data
from static_text import messages


# Define a function that raises an error if input is not YouTube url
def validate_input(user_message):
    if not user_message.startswith('https://youtu.be') and not user_message.startswith('https://www.youtube'):
        raise ValueError(f"{messages[manage_data.selected_language]['check_url_text']}")


def is_supported(url):
    extractors = yt_dlp.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(url) and e.IE_NAME != 'generic':
            return True
    return False
