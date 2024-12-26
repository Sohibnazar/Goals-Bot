from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,ContextTypes
from config import TOKEN
from database import init_db, add_goal, add_task

# Инициализация базы данных
init_db()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>Привет! 🎯 Я помогу вам отслеживать цели. Используйте команды:</b>\n"
         "\n"
        "➕ <b>/add_goal   -   Добавить цель </b>\n"
        "\n"
        "📋 <b>/add_task   -    Добавить подзадачу к цели</b>\n",
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
            "\n"
            f"🔹<b> **Описание:** </b> {description_1}\n"
            "\n"
            f"📅 <b> **Дедлайн:**</b> {deadline}\n"
            "\n"
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
            "     <code>  <b>/add_goal    'Изучить Python'    '2024-12-31'</b></code>",
            parse_mode='HTML'
        )

# Команда /add_task
async def add_task_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получаем аргументы
        description = ' '.join(context.args[0:-2])  # Объединяем все слова, кроме даты
        deadline = context.args[-2]  # Последний аргумент - дедлайн
        goal_id = int(context.args[-1])  # ID цели

        # Добавляем задачу в базу данных
        add_task(goal_id, description, deadline)

        # Сообщение об успехе
        await update.message.reply_text(
            f"✅ <b>Задача успешно добавлена!</b>\n\n" 
            f"🔹 <b>Цель goal_id:</b> <code>{goal_id}</code>\n"
             "\n"
            f"📝 <b>Описание задачи:</b> {description}\n"
             "\n"
            f"📅 <b>Дедлайн:</b> {deadline}\n\n"
            
            f"💡 <i>Не забудьте проверить статус с помощью /view_tasks!</i>",
            parse_mode='HTML'  # Включаем HTML-разметку
        )
    except Exception as e:
        # Сообщение об ошибке
        await update.message.reply_text(
            "📜 <b>Используйте правильный формат для добавления задачи:</b>\n"
            "\n"
            "📋 <b>/add_task  'Описание задачи'   YYYY-MM-DD   goal_id  </b>\n\n"
            "<b><i>Пример:</i></b>\n"
            "<code><b>/add_task 'Прочитать книгу по Python' 2024-12-31  1 </b></code>",
            parse_mode='HTML'
        )


# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add_goal", add_goal_command))
app.add_handler(CommandHandler("add_task", add_task_command))


print("Бот запущен!")
app.run_polling()
