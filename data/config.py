import os
import re
from dotenv import load_dotenv

load_dotenv()

# Token бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# id владельцев бота
owners = [
    139653633,
]

# Данные подключения к базе данных postgresql
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Приставка для имён схем базы данных
SCHEMA = 'schema_'

# Имена таблиц
MESSAGES_STRUCT = 'messages_struct'
MESSAGES_UNSTRUCT = 'messages_unstruct'
DICT_PROBLEMS = 'dict_problems'
DICT_ADMINS = 'dict_admins'
DICT_USERS = 'dict_users'

# Паттерн @user_id
PATTERN_ID = re.compile(r'[0-9]+')

# Паттерн @user_name
# PATTERN_USER_NAME = re.compile(r'@[a-zA-Z][a-zA-Z0-9\_]{4,}')
