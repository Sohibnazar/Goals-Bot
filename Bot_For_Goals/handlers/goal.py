from Bot_For_Goals.database.database import add_goal,complete_goal,delete_goal
from Bot_For_Goals.handlers.keyboards import back_to_start,back_to_goals_menu
from Bot_For_Goals.handlers.messages import  *
from datetime import datetime
import re

async def get_goal_data(update, context):
    user_input = update.message.text
    match = re.match(r"^(.*?)\s+(\d{4}-\d{2}-\d{2})$", user_input)
    if match:
        description = match.group(1)
        deadline_str = match.group(2)
        user_id = str(update.message.chat_id)
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            goal_id = add_goal(description, deadline, user_id)
            if goal_id:
                await update.message.reply_text(
                    GOAL_ADDED_SUCCESS.format(description=description, deadline=deadline),
                    parse_mode='HTML',
                    reply_markup=back_to_goals_menu
                )
            else:
                await update.message.reply_text(GOAL_ADD_FAILED, reply_markup=back_to_goals_menu)
        except Exception as e:
            print(f"Ошибка при добавлении цели: {e}")
            await update.message.reply_text(ERROR_DATE_FORMAT, reply_markup=back_to_goals_menu)
    else:
        await update.message.reply_text(ERROR_ID_NOT_FOUND, reply_markup=back_to_goals_menu)

async def mark_goal_complete(update, context):
    user_input = update.message.text.strip()
    try:
        match = re.search(r'\b\d+\b', user_input)
        if match:
            goal_id = int(match.group())
            result = complete_goal(goal_id)
            if result:
                await update.message.reply_text(
                    GOAL_COMPLETED_SUCCESS.format(goal_id=goal_id),
                    parse_mode='HTML',
                    reply_markup=back_to_goals_menu
                )
            elif result == "already_completed":
                await update.message.reply_text(
                    ERROR_GOAL_ALREADY_COMPLETED.format(goal_id=goal_id),
                    reply_markup=back_to_goals_menu
                )
            else:
                await update.message.reply_text(
                    ERROR_GOAL_NOT_FOUND.format(goal_id=goal_id),
                    reply_markup=back_to_goals_menu
                )
        else:
            await update.message.reply_text(ERROR_ID_NOT_FOUND, reply_markup=back_to_goals_menu)
    except Exception as e:
        print(f"Ошибка при выполнении цели: {e}")
        await update.message.reply_text(ERROR_GENERIC, reply_markup=back_to_goals_menu)

async def mark_goal_delete(update, context):
    user_input = update.message.text.strip()
    try:
        match = re.search(r'\b\d+\b', user_input)
        if match:
            goal_id = int(match.group())
            success = delete_goal(goal_id)
            if success:
                await update.message.reply_text(
                    GOAL_DELETED_SUCCESS.format(goal_id=goal_id),
                    parse_mode='HTML',
                    reply_markup=back_to_start
                )
            else:
                await update.message.reply_text(
                    ERROR_GOAL_NOT_FOUND.format(goal_id=goal_id),
                    reply_markup=back_to_start
                )
        else:
            await update.message.reply_text(ERROR_ID_NOT_FOUND, reply_markup=back_to_start)
    except Exception as e:
        print(f"Ошибка при удалении цели: {e}")
        await update.message.reply_text(ERROR_GENERIC, reply_markup=back_to_start)