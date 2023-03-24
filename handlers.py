from errors import validate_input, is_supported
from static_text import messages, welcome_text, wait_text, help_text, undefined_command_text, messages
from service import get_info, download
from keyboards import formats_keyboard, lang_keyboard
from manage_data import id_dict
import manage_data


async def start(update, context):
    """Send a message when the command /start is issued."""
    user_lang = update.message.from_user.language_code
    if user_lang not in messages:
        user_lang = 'en'
    await update.message.reply_text(messages[user_lang]["welcome_text"])
    await update.message.reply_text(
        text=messages[user_lang]["select_lang_text"],
        reply_markup=lang_keyboard()
    )


async def language_handler(update, context):
    selected_lang = update.callback_query["data"].split(".")[-1]
    manage_data.selected_language = selected_lang
    await update.callback_query.message.edit_text(messages[manage_data.selected_language]["selected_lang_text"])


async def audio_url_handler(update, context):
    """Send a message when the command /download_mp3 is issued."""
    nick, name, user_id, lang, date = update.message.from_user.username, update.message.from_user.first_name, \
                                      update.message.from_user.id, update.message.from_user.language_code, \
                                      update.message.date
    user_link = update.message.text
    message_id = update.message.message_id
    # print(f"Request from USER {nick} (first name is {name}). User id {user_id}, language {lang}. "
    #       f"Request text: {user_link}")
    # print(update.message.date)
    id_dict[message_id] = []
    id_dict[message_id].append(user_link)
    with open("log_file.csv", "a", encoding="windows-1251") as log:
        log.write(f"{date},{nick},{name},{user_id},{lang},{user_link}\n")
    if is_supported(user_link):
        await update.message.reply_text(messages[manage_data.selected_language]["wait_text"])
        message = get_info(message_id, user_link)
        await context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            message_id=update.message.message_id + 1,  # +1
            text=message
        )
        await update.message.reply_text(
            text=messages[manage_data.selected_language]["select_format_text"],
            reply_markup=formats_keyboard()
        )
    else:
        await update.message.reply_text(messages[manage_data.selected_language]["check_url_text"])

    # try:
    #     is_supported(user_link)
    # except ValueError as e:
    #     await update.message.reply_text(str(e))
    # except YoutubeDLError as e:
    #     await update.message.reply_text(str(e))
    # else:
    #     await update.message.reply_text(messages[manage_data.selected_language]["wait_text"])
    #     message = get_info(message_id, user_link)
    #     await context.bot.edit_message_text(
    #         chat_id=update.message.chat_id,
    #         message_id=update.message.message_id + 1,  # +1
    #         text=message
    #     )
    #     await update.message.reply_text(
    #         text=messages[manage_data.selected_language]["select_format_text"],
    #         reply_markup=formats_keyboard()
    #     )


async def format_download_handler(update, context):
    message_id = update.callback_query.message.message_id
    await update.callback_query.message.edit_text(wait_text)
    audio_format = update.callback_query["data"].split(".")[-1]
    audio_file = download(id_dict[message_id-2][0], id_dict[message_id-2][1], audio_format)
    await context.bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,  # +1
        text=messages[manage_data.selected_language]["ready_notification_text"]
    )
    print(audio_file)

    await context.bot.send_document(chat_id=update.callback_query.message.chat_id,
                                    document=audio_file,
                                    timeout=7200
                                    )
    id_dict[message_id-2].append("Success")
    print(id_dict)
    with open("log_success.csv", "a", encoding="windows-1251") as log:
        for k, v in id_dict.items():
            k = str(k)
            if len(v) == 3:
                stroke = f"{str(k)},{v[0]},{v[1]},{v[2]}\n"
                log.write(stroke)
            if len(v) == 2:
                stroke = f"{str(k)},{v[0]},{v[1]}\n"
                log.write(stroke)

    # with open("log_file.csv", "a") as log:
    #     log.write("Success!\n")
    # print("Success!")


# Standard functionality
async def helper(update, context):
    text = messages[manage_data.selected_language]["help_text"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def undefined_commands(update, context):
    text = messages[manage_data.selected_language]["undefined_command_text"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
