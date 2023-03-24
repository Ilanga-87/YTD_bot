from errors import validate_input
from static_text import welcome_text, help_text, undefined_command_text, wait_text
from service import get_info, download
from keyboards import formats_keyboard
from manage_data import yt_url


async def start(update, context):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(welcome_text)


async def audio(update, context):
    """Send a message when the command /download_mp3 is issued."""
    if len(yt_url) > 0:
        yt_url.clear()
    nick, name, user_id, lang, date = update.message.from_user.username, update.message.from_user.first_name, \
                                      update.message.from_user.id, update.message.from_user.language_code, \
                                      update.message.date
    user_link = update.message.text
    message_id = update.message.message_id
    # print(f"Request from USER {nick} (first name is {name}). User id {user_id}, language {lang}. "
    #       f"Request text: {user_link}")
    # print(update.message.date)
    print(message_id)
    with open("log_file.csv", "a") as log:
        log.write(f"{date},{nick},{name},{user_id},{lang},{user_link}\n")
    try:
        pass
        validate_input(user_link)
    except ValueError as e:
        await update.message.reply_text(str(e))
    else:
        await update.message.reply_text(wait_text)
        yt_url.append(user_link)
        message = get_info(user_link)
        await context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            message_id=update.message.message_id + 1,  # +1
            text=message
        )
        await update.message.reply_text(
            text="Select preferred audio format to download: ",
            reply_markup=formats_keyboard()
        )


async def select_format(update, context):
    await update.callback_query.message.edit_text(wait_text)
    audio_format = update.callback_query["data"].split(".")[-1]
    audio_file = download(yt_url[0], yt_url[1], audio_format)
    yt_url.clear()
    await context.bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,  # +1
        text="It's ready"
    )
    print(audio_file)

    await context.bot.send_document(chat_id=update.callback_query.message.chat_id,
                                    document=audio_file
                                    )


# Standard functionality
async def helper(update, context):
    text = help_text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def undefined_commands(update, context):
    text = undefined_command_text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
