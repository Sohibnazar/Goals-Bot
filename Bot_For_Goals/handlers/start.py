from Bot_For_Goals.handlers.messages import WELCOME_MESSAGE
from Bot_For_Goals.handlers.keyboards import  main_menu
from Bot_For_Goals.logs.logger import logger
from telegram.ext import ContextTypes
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"Получено сообщение от пользователя {user.id} ({user.full_name}, @{user.username}): /start")
    await update.message.reply_text(
        WELCOME_MESSAGE,
        parse_mode='HTML',
        reply_markup=main_menu
    )
