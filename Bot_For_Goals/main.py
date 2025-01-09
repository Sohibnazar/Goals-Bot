from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers.task import get_tasks_for_goal,mark_task_complete,view_task,mark_task_delete
from handlers.goal import get_goal_data, mark_goal_complete,mark_goal_delete
from Bot_For_Goals.handlers.messages import  ERROR_UNKNOWN_COMMAND
from Bot_For_Goals.handlers.keyboards import back_to_start
from Bot_For_Goals.handlers.scheduler import scheduler
from Bot_For_Goals.logs.logger import logger
from config.config import TOKEN
from handlers.start import start
from handlers.button import button

async def check_message(update, context):
    user = update.message.from_user
    user_input = update.message.text.lower()
    logger.info(f"Получено сообщение от пользователя {user.id} ({user.full_name}, @{user.username}): {user_input}")

    try:
        if 'цель' in user_input:
            await get_goal_data(update, context)
        elif 'задача' in user_input:
            await get_tasks_for_goal(update, context)
        elif 'goal id:' in user_input:
            await mark_goal_complete(update, context)
        elif 'del id:' in user_input:
            await mark_goal_delete(update, context)
        elif 'task id:' in user_input:
            await mark_task_complete(update, context)
        elif 'del task:' in user_input:
            await mark_task_delete(update, context)
        elif 'id:' in user_input:
            await view_task(update, context)
        else:
            logger.warning(f"Неизвестная команда от пользователя {user.id} ({user.full_name}, @{user.username}): {user_input}")
            await update.message.reply_text(
                ERROR_UNKNOWN_COMMAND,
                parse_mode='HTML',
                reply_markup=back_to_start
            )
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения от пользователя {user.id} ({user.full_name}, @{user.username}): {e}")
        await update.message.reply_text(
            "Произошла ошибка, пожалуйста, попробуйте снова позже.",
            parse_mode='HTML',
            reply_markup=back_to_start
        )

def run():
    try:
        scheduler.start()
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CallbackQueryHandler(button))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
        app.run_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    run()