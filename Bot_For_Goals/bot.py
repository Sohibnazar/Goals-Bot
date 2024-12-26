from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,ContextTypes
from config import TOKEN
from database import init_db, add_goal

# Инициализация базы данных
init_db()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>Привет! 🎯 Я помогу вам отслеживать цели. Используйте команды:</b>\n"
         "\n"
        "➕ <b>/add_goal   -   Добавить цель </b>\n",
        parse_mode='HTML'
    )

# Команда /add_goal
async def add_goal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        description = context.args[0]
        description_1 = context.args[1]
        deadline = context.args[2]
        add_goal(description, deadline)
        await update.message.reply_text(
            f"🎯 <b> Цель успешно добавлена! </b>\n"
            f"🔹<b> **Описание:** </b>{description} {description_1}\n"
            f"📅 <b> **Дедлайн:**</b> {deadline}\n"
            "<b> Вы можете отслеживать её с помощью команды /view_goals.</b>",
            parse_mode='HTML'
        )
    except:
        await update.message.reply_text(
            "📜 <b>Пожалуйста, используйте правильный формат для добавления цели:</b>\n"
            "\n"
            "➕ <b>/add_goal   'Описание цели'   'YYYY-MM-DD'</b>\n"
            "\n"
            "<b><i>💡 Пример:</i></b>\n"
            "       <b>/add_goal    'Изучить Python'    '2024-12-31'</b>",
            parse_mode='HTML'
        )


# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add_goal", add_goal_command))


print("Бот запущен!")
app.run_polling()
