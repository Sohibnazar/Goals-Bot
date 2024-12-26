from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,ContextTypes
from config import TOKEN
from database import init_db, add_goal

# Инициализация базы данных
init_db()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу вам отслеживать цели. Используйте команды:\n"
        "/add_goal - Добавить цель\n"
    )

# Команда /add_goal
async def add_goal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        description = context.args[0]
        description_1 = context.args[1]
        deadline = context.args[2]
        add_goal(description, deadline)
        await update.message.reply_text(f"Цель '{description} {description_1}' добавлена с дедлайном {deadline}!")
    except:
        await update.message.reply_text("Используйте формат: /add_goal   'Описание'    YYYY-MM-DD")



# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add_goal", add_goal_command))


print("Бот запущен!")
app.run_polling()
