from telegram.ext import ConversationHandler,ContextTypes
from Bot_For_Goals.database.database import  get_goals,get_statistics,check_goal_exists
from Bot_For_Goals.logs.logger import logger
from datetime import datetime
from Bot_For_Goals.handlers.keyboards import  (
    main_menu,
    back_to_start,
    goal_menu,
    back_to_goals_menu
)
from Bot_For_Goals.handlers.messages import (
    WELCOME_MESSAGE,
    BACK_MESSAGE_GOAL,
    ERROR_MESSAGE,
    ADD_GOAL_MESSAGE,
    ADD_TASK_MESSAGE,
    COMPLETE_GOAL_MESSAGE,
    DELETE_GOAL_MESSAGE,
    VIEW_TASKS_MESSAGE,
    COMPLETE_TASK_MESSAGE,
    DELETE_TASK_MESSAGE,
    NO_GOALS_MESSAGE,
    QUOTES_COMPLETED_GOAL,
    QUOTES_FAILED,
    QUOTES_ADD_TASK,
    QUOTES_ADD_GOAL,
    QUOTES_VIEW_TASKS,
    QUOTES_COMPLETE_TASK,
    QUOTES_DELETE,
    QUOTES_STATS,
    QUOTES_IN_PROGRESS

)
import random

async def button(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    logger.info(f"Пользователь {user.id} ({user.full_name}, @{user.username}) нажал кнопку: {query.data}")
    await query.answer()
    data = query.data
    if data == 'add_goal':
        quote = random.choice(QUOTES_ADD_GOAL)
        await query.edit_message_text(
            text=f"{ADD_GOAL_MESSAGE}\n\n💬 <i>{quote}</i>",
            parse_mode='HTML',
            reply_markup=back_to_start
        )
        return 'ADDING_GOAL'

    elif data == 'add_task':
        user_id = query.from_user.id
        if check_goal_exists(user_id):
            quote = random.choice(QUOTES_ADD_TASK)
            await query.edit_message_text(
                text=f"{ADD_TASK_MESSAGE}\n\n💬 <i>{quote}</i>",
                parse_mode='HTML',
                reply_markup=back_to_start
            )
            return 'ADDING_TASK'

        else:
            await query.edit_message_text(
                text=NO_GOALS_MESSAGE,
                parse_mode='HTML',
                reply_markup=back_to_start
            )
            return 'WAITING_FOR_GOAL'

    elif data == 'back_to_start':
        await query.edit_message_text(
            text=f"{WELCOME_MESSAGE}\n\n",
            parse_mode='HTML',
            reply_markup=main_menu
        )
        return ConversationHandler.END

    elif data == 'view_goals':
        try:
            goals = get_goals()
            if goals:
                current_date = datetime.now().date()
                all_goals_response = ""
                for goal in goals:
                    deadline_date = goal.deadline
                    if goal.completed:
                        status = "✅ Выполнена"
                        quote = random.choice(QUOTES_COMPLETED_GOAL)
                    elif deadline_date < current_date:
                        status = "❌ Просрочена"
                        quote = random.choice(QUOTES_FAILED)
                    else:
                        status = "⏳ В процессе"
                        quote = random.choice(QUOTES_IN_PROGRESS)
                    goal_response = f"🔑 <b>ID:</b> <code>{goal.id}</code>\n\n"
                    goal_response += f"🎯 <b>{goal.title}</b>\n\n"
                    goal_response += f"📅 <b>Дедлайн:</b> {goal.deadline}\n\n"
                    goal_response += f"{status}\n\n"
                    goal_response += f"💬 <i>{quote}</i>\n\n"
                    goal_response += f"{'-' * 102}\n"
                    all_goals_response += goal_response
                await query.edit_message_text(
                    all_goals_response + "\n\n",
                    parse_mode='HTML',
                    reply_markup=goal_menu
                )
            else:
                await query.edit_message_text(
                    f"{BACK_MESSAGE_GOAL}\n\n",
                    parse_mode='HTML',
                    reply_markup=back_to_start
                )
            return ConversationHandler.END
        except Exception as e:
            await query.edit_message_text(f"{ERROR_MESSAGE}{str(e)}")
            return ConversationHandler.END

    elif data == 'complete_goal':
        quote = random.choice(QUOTES_COMPLETED_GOAL)
        await query.edit_message_text(
            text=f"{COMPLETE_GOAL_MESSAGE}\n\n💬 <i>{quote}</i>",
            parse_mode='HTML',
            reply_markup=back_to_goals_menu
        )
        return 'COMPLETING_ID'

    elif data == 'delete_goal':
        quote = random.choice(QUOTES_DELETE)
        await query.edit_message_text(
            text=f"{DELETE_GOAL_MESSAGE}\n\n💬 <i>{quote}</i>",
            parse_mode='HTML',
            reply_markup=back_to_goals_menu
        )
        return 'DELITING_ID'

    elif data == 'view_tasks':
        quote = random.choice(QUOTES_VIEW_TASKS)
        await query.edit_message_text(
            text=f"{VIEW_TASKS_MESSAGE}\n\n💬 <i>{quote}</i>",
            parse_mode='HTML',
            reply_markup=back_to_goals_menu
        )
        return 'TASKS_ID'

    elif data == 'complete_task':
        quote = random.choice(QUOTES_COMPLETE_TASK)
        await query.edit_message_text(
            text=f"{COMPLETE_TASK_MESSAGE}\n\n💬 <i>{quote}</i>",
            parse_mode='HTML',
            reply_markup=back_to_goals_menu
        )
        return 'COMPLETING_ID'

    elif data == 'delete_task':
        quote = random.choice(QUOTES_DELETE)
        await query.edit_message_text(
            text=f"{DELETE_TASK_MESSAGE}\n\n💬 <i>{quote}</i>",
            parse_mode='HTML',
            reply_markup=back_to_goals_menu
        )
        return 'DELITING_ID'

    elif data == 'view_stats':
        quote = random.choice(QUOTES_STATS)
        stats = get_statistics()
        if stats:
            stats_text = (
                f"<b>📊 Статистика:</b>\n\n"
                f"<b>🎯 Цели:</b>\n\n"
                f"Всего: {stats['total_goals']}\n\n"
                f"✅ Выполнено: {stats['completed_goals']} ({stats['goal_percent']:.2f}%)\n\n"
                f"❌ Невыполнено: {stats['incomplete_goals']}\n\n"
                f"<b>📋 Задачи:</b>\n\n"
                f"Всего: {stats['total_tasks']}\n\n"
                f"✅ Выполнено: {stats['completed_tasks']} ({stats['task_percent']:.2f}%)\n\n"
                f"❌ Невыполнено: {stats['incomplete_tasks']}\n"
            )
            await query.edit_message_text(
                text=f"{stats_text}\n\n💬 <i>{quote}</i>",
                parse_mode="HTML",
                reply_markup=back_to_start
            )
        else:
            await query.edit_message_text(
                f"Не удалось получить статистику.\n\n💬 <i>{quote}</i>",
                parse_mode="HTML"
            )
