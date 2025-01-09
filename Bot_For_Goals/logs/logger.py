import logging
import os
if not os.path.exists('logs'):
    os.makedirs('logs')

logger = logging.getLogger('bot_logger')

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('logs/bot_logs.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("Бот запущен")
