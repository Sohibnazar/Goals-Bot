from Bot_For_Goals.database.database import add_task, complete_task,get_tasks,delete_task
from Bot_For_Goals.handlers.keyboards import  back_to_start,back_to_goals_menu
from Bot_For_Goals.handlers.keyboards import task_menu
from Bot_For_Goals.handlers.messages import  *
from datetime import datetime
import re

async def get_tasks_for_goal(update, context):
    user_input = update.message.text.strip()
    match = re.match(r"^(.*?)\s+(\d{4}-\d{2}-\d{2})\s+(\d+)$", user_input)
    if match:
        description = match.group(1)
        deadline_str = match.group(2)
        goal_id = int(match.group(3))
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            task_id = add_task(description, deadline, goal_id)
            if task_id:
                await update.message.reply_text(
                    TASK_ADDED_SUCCESS.format(description=description, deadline=deadline, goal_id=goal_id),
                    parse_mode='HTML',
                    reply_markup=back_to_goals_menu
                )
            elif task_id is None:
                await update.message.reply_text(
                    TASK_GOAL_NOT_FOUND.format(goal_id=goal_id),
                    reply_markup=back_to_start
                )
            else:
                await update.message.reply_text(TASK_ADD_FAILED, reply_markup=back_to_start)
        except ValueError:
            await update.message.reply_text(ERROR_DATE_FORMAT, reply_markup=back_to_start)
        except Exception as e:
            print(f"Ошибка при добавлении задачи: {e}")
            await update.message.reply_text(ERROR_GENERIC, reply_markup=back_to_start)
    else:
        await update.message.reply_text(ERROR_ID_NOT_FOUND, reply_markup=back_to_start)

async def mark_task_complete(update, context):
    user_input = update.message.text.strip()
    try:
        match = re.search(r'\b\d+\b', user_input)
        if match:
            task_id = int(match.group())
            result = complete_task(task_id)
            if result:
                await update.message.reply_text(
                    TASK_COMPLETED_SUCCESS.format(task_id=task_id),
                    parse_mode='HTML',
                    reply_markup=back_to_goals_menu
                )
            elif result == "already_completed":
                await update.message.reply_text(
                    ERROR_TASK_ALREADY_COMPLETED.format(task_id=task_id),
                    reply_markup=back_to_goals_menu
                )
            else:
                await update.message.reply_text(
                    ERROR_TASK_NOT_FOUND.format(task_id=task_id),
                    reply_markup=back_to_goals_menu
                )
        else:
            await update.message.reply_text(ERROR_TASK_ID_NOT_FOUND, reply_markup=back_to_goals_menu)
    except Exception as e:
        print(f"Ошибка при выполнении задачи: {e}")
        await update.message.reply_text(ERROR_GENERIC, reply_markup=back_to_goals_menu)

async def mark_task_delete(update, context):
    user_input = update.message.text.strip()
    try:
        match = re.search(r'\b\d+\b', user_input)
        if match:
            task_id = int(match.group())
            success = delete_task(task_id)
            if success:
                await update.message.reply_text(
                    TASK_DELETED_SUCCESS.format(task_id=task_id),
                    parse_mode='HTML',
                    reply_markup=back_to_goals_menu
                )
            else:
                await update.message.reply_text(
                    ERROR_TASK_NOT_FOUND.format(task_id=task_id),
                    reply_markup=back_to_goals_menu
                )
        else:
            await update.message.reply_text(ERROR_ID_NOT_FOUND, reply_markup=back_to_goals_menu)
    except Exception as e:
        print(f"Ошибка при удалении задачи: {e}")
        await update.message.reply_text(ERROR_GENERIC, reply_markup=back_to_goals_menu)

async def view_task(update, context):
    user_input = update.message.text.strip()
    try:
        match = re.search(r'\b\d+\b', user_input)
        if match:
            goal_id = int(match.group())
            tasks = get_tasks(goal_id)
            if tasks:
                current_date = datetime.now().date()
                all_tasks_response = ""
                for task in tasks:
                    status = "✅ Выполнена" if task.completed else "❌ Просрочена" if task.deadline < current_date else "⏳ В процессе"
                    all_tasks_response += (
                        f"🔹 <b>ID:</b> <code>{task.id}</code>\n\n"
                        f"📝 <b>{task.title}</b>\n\n"
                        f"📅 <b>Дедлайн:</b> {task.deadline}\n\n"
                        f"{status}\n\n{'-' * 102}\n"
                    )
                await update.message.reply_text(
                    all_tasks_response + TASK_LIST_FOOTER,
                    parse_mode='HTML',
                    reply_markup=task_menu
                )
            else:
                await update.message.reply_text(NO_TASKS_MESSAGE, parse_mode='HTML', reply_markup=back_to_goals_menu)
        else:
            await update.message.reply_text(ERROR_ID_NOT_FOUND, reply_markup=back_to_goals_menu)
    except Exception as e:
        print(f"Ошибка при выводе задач: {e}")
        await update.message.reply_text(ERROR_GENERIC, reply_markup=back_to_goals_menu)

