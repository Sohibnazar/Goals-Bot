from apscheduler.schedulers.background import BackgroundScheduler
from Bot_For_Goals.database.database import session,Task
from Bot_For_Goals.config.config import TOKEN
from Bot_For_Goals.handlers.messages import REMINDER_MESSAGE
from datetime import datetime, timedelta
from telegram import Bot
import asyncio

bot = Bot(token=TOKEN)

async def check_deadlines():
    tomorrow = datetime.now().date() + timedelta(days=1)
    tasks = session.query(Task).filter(Task.deadline == tomorrow, Task.completed == False).all()

    for task in tasks:
        user_id = task.goal.user_id
        await bot.send_message(
            chat_id=user_id,
            text=REMINDER_MESSAGE.format(task_title=task.title),
            parse_mode='HTML'
        )

def run_check_deadlines():
    asyncio.run(check_deadlines())

scheduler = BackgroundScheduler()
scheduler.add_job(run_check_deadlines, 'cron', hour=8, minute=0)
scheduler.add_job(run_check_deadlines, 'cron', hour=12, minute=0)
scheduler.add_job(run_check_deadlines, 'cron', hour=18, minute=0)