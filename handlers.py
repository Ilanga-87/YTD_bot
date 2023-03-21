from errors import validate_input
from static_text import welcome_text, help_text, undefined_command_text, wait_text
from service import get_info
from keyboards import formats_keyboard


async def start(update, context):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(welcome_text)


async def download_mp3(update, context):
    """Send a message when the command /download_mp3 is issued."""
    user_link = " ".join(context.args)
    try:
        validate_input(user_link)
    except ValueError as e:
        await update.message.reply_text(str(e))
    else:
        await update.message.reply_text(wait_text)
        message = get_info(user_link)
        await context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            message_id=update.message.message_id+1,
            text=message
        )
        await update.message.reply_text(
            text="Select preferred audio format to download: ",
            reply_markup=formats_keyboard()
        )


async def helper(update, context):
    text = help_text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def undefined_commands(update, context):
    text = undefined_command_text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
