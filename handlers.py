from telegram.error import NetworkError, BadRequest

from errors import is_supported
from static_text import wait_text, messages
from service import get_info, download, download_long
from keyboards import formats_keyboard, lang_keyboard, mp3_keyboard
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
    manage_data.huge_file_flag = False
    manage_data.long_file_flag = False
    nick, name, user_id, lang, date = update.message.from_user.username, update.message.from_user.first_name, \
                                      update.message.from_user.id, update.message.from_user.language_code, \
                                      update.message.date
    user_link = update.message.text
    message_id = update.message.message_id
    # print(f"Request from USER {nick} (first name is {name}). User id {user_id}, language {lang}. "
    #       f"Request text: {user_link}")
    # print(update.message.date)
    manage_data.id_dict[message_id] = []
    manage_data.id_dict[message_id].append(user_link)
    manage_data.id_dict[message_id].append(nick)
    manage_data.id_dict[message_id].append(name)
    manage_data.id_dict[message_id].append(user_id)
    manage_data.id_dict[message_id].append(lang)
    manage_data.id_dict[message_id].append(date)

    with open("log_file.csv", "a", encoding="windows-1251") as log:
        log.write(f"{date},{nick},{name},{user_id},{lang},{user_link}\n")
    if is_supported(user_link):
        await update.message.reply_text(messages[manage_data.selected_language]["wait_text"])
        message = get_info(message_id, user_link)
        if not manage_data.huge_file_flag:
            await context.bot.edit_message_text(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id + 1,  # +1
                text=message
            )
            if not manage_data.long_file_flag:
                await update.message.reply_text(
                    text=messages[manage_data.selected_language]["select_format_text"],
                    reply_markup=formats_keyboard()
                )
            else:
                await context.bot.edit_message_text(
                    chat_id=update.message.chat_id,
                    message_id=update.message.message_id + 1,  # +1
                    text=message,
                    reply_markup=mp3_keyboard()
                )
        else:
            await context.bot.edit_message_text(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id + 1,  # +1
                text=message
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
    print(message_id)
    print(f"The file is long: {manage_data.long_file_flag}")
    await update.callback_query.message.edit_text(wait_text)
    audio_format = update.callback_query["data"].split(".")[-1]
    if manage_data.long_file_flag:
        audio_file = download_long(manage_data.id_dict[message_id-1][0], manage_data.id_dict[message_id-1][6], audio_format)
    else:
        audio_file = download(manage_data.id_dict[message_id-2][0], manage_data.id_dict[message_id-2][6], audio_format)

    print(audio_file)
    try:
        await context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,  # +1
            text=messages[manage_data.selected_language]["ready_notification_text"]
        )
        await context.bot.send_document(chat_id=update.callback_query.message.chat_id,
                                        document=audio_file,
                                        read_timeout=7200,
                                        write_timeout=7200
                                        )
        # manage_data.id_dict[message_id - 2].append("Success")
        if manage_data.id_dict.get(message_id - 2, None) is None:
            manage_data.id_dict[message_id - 1].append("Success")
        else:
            manage_data.id_dict[message_id - 2].append("Success")

        print(manage_data.id_dict)
        with open("log_success.csv", "w", encoding="windows-1251") as log:
            for k, v in manage_data.id_dict.items():
                k = str(k)
                if len(v) == 3:
                    stroke = f"{str(k)},{v[0]},{v[1]},{v[2]}\n"
                    log.write(stroke)
                if len(v) == 2:
                    stroke = f"{str(k)},{v[0]},{v[1]}\n"
                    log.write(stroke)
    except BadRequest as br_error:
        error_text = str(br_error).split(": ")[-1].strip()
        if manage_data.id_dict.get(message_id - 2, None) is None:
            manage_data.id_dict[message_id - 1].append(error_text)
        else:
            manage_data.id_dict[message_id - 2].append(error_text)
        with open("log_success.csv", "w", encoding="windows-1251") as log:
            for k, v in manage_data.id_dict.items():
                k = str(k)
                if len(v) == 3:
                    stroke = f"{str(k)},{v[0]},{v[1]},{v[2]}\n"
                    log.write(stroke)
                if len(v) == 2:
                    stroke = f"{str(k)},{v[0]},{v[1]}\n"
                    log.write(stroke)
        print(error_text)
        await context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,  # +1
            text=messages[manage_data.selected_language]["wrong_url_text"]
        )
    except NetworkError as ne:
        error_text = str(ne).split(": ")[-1].strip()
        if manage_data.id_dict.get(message_id - 2, None) is None:
            manage_data.id_dict[message_id - 1].append(error_text)
        else:
            manage_data.id_dict[message_id - 2].append(error_text)
        with open("log_success.csv", "w", encoding="windows-1251") as log:
            for k, v in manage_data.id_dict.items():
                k = str(k)
                if len(v) == 3:
                    stroke = f"{str(k)},{v[0]},{v[1]},{v[2]}\n"
                    log.write(stroke)
                if len(v) == 2:
                    stroke = f"{str(k)},{v[0]},{v[1]}\n"
                    log.write(stroke)
        print(error_text)
        await context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,  # +1
            text=messages[manage_data.selected_language]["you_tube_error_text"]
        )


# Standard functionality
async def helper(update, context):
    text = messages[manage_data.selected_language]["help_text"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def undefined_commands(update, context):
    text = messages[manage_data.selected_language]["undefined_command_text"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
