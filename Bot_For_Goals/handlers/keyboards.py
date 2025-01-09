from telegram import InlineKeyboardButton, InlineKeyboardMarkup

main_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Добавить цель", callback_data='add_goal'),
     InlineKeyboardButton("📋 Добавить подзадачу", callback_data='add_task')],
    [InlineKeyboardButton("📜 Посмотреть все цели", callback_data='view_goals'),
     InlineKeyboardButton("📊 Статистика", callback_data='view_stats')]
])

back_to_start = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Назад", callback_data='back_to_start')]
])

goal_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("✅ Выполнено", callback_data='complete_goal')],
    [InlineKeyboardButton("📝 Список подзадачи", callback_data='view_tasks'),
     InlineKeyboardButton("❌ Удалить", callback_data='delete_goal')],
    [InlineKeyboardButton("🔙 Назад", callback_data='back_to_start')]
])
task_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("✅ Выполнено", callback_data='complete_task'),
    InlineKeyboardButton("❌ Удалить", callback_data='delete_task')],
    [InlineKeyboardButton("🔙 Назад", callback_data='view_goals')]
])
back_to_goals_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔙 Назад", callback_data='view_goals')]
])
