from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.dispatcher.filters import Regexp

from data import config
from loader import database
from loader import dispatcher
import emoji


@dispatcher.message_handler(Regexp(config.PATTERN_PROBLEM))
async def rec_re(message: types.Message):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    if await database.exists_schema(schema_name):
        result_problem = config.PATTERN_PROBLEM.search(message.text)
        dict_problem = result_problem.group(0).split('/')
        message_id = message.message_id
        try:
            reply_id = message.reply_to_message.message_id
        except:
            reply_id = 0
        hub = dict_problem[0].replace('#', '')
        city = dict_problem[1].replace(' ', '')
        number_problem = dict_problem[2]
        user_id = message.from_user.id
        full_name = message.from_user.full_name
        user_name = message.from_user.username
        message_text = message.text
        date_time = message.date
        sql = f"""INSERT INTO {schema_name}.{config.TABLE_STRUCT_MESSAGES} 
            (message_id, reply_id, hub, city, number_problem, user_id, full_name, user_name, message_text, date_time)
            VALUES ({message_id}, {reply_id}, {hub}, '{city}', {number_problem}, {user_id}, '{full_name}', 
                '{user_name}', '{message_text}', '{date_time}')
        """
        await database.execute(sql, execute=True)
    else:
        pass


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT))
async def rec_rest(message: types.Message):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    if await database.exists_schema(schema_name):
        message_id = message.message_id
        try:
            reply_id = message.reply_to_message.message_id
        except:
            reply_id = 0
        user_id = message.from_user.id
        full_name = message.from_user.full_name
        user_name = message.from_user.username
        message_text = message.text
        date_time = message.date
        sql = f"""INSERT INTO {schema_name}.{config.TABLE_UNSTRUCT_MESSAGES}
            (message_id, reply_id, user_id, full_name, user_name, message_text, date_time)
            VALUES ({message_id}, {reply_id}, {user_id}, '{full_name}', '{user_name}', '{message_text}', '{date_time}')
        """
        await database.execute(sql, execute=True)
        list_of_dicts_operators = await database.get_list_operators(schema_name)
        if not any(d['operator_id'] == message.from_user.id for d in list_of_dicts_operators):
            message_from = message.from_user.full_name
            answer = await message.answer(emoji.emojize(':warning: ') +
                                          f'<code>{message_from}</code>, пожалуйста, пишите '
                                          f'сообщения в соответствии с правилами!')
            await database.add_service_message(schema_name, answer.message_id)
            await message.delete()
        else:
            pass
    else:
        pass


@dispatcher.message_handler(content_types=types.ContentType.all())
async def delete_message(message: types.Message):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    if await database.exists_schema(schema_name):
        dict_operators = await database.get_list_operators(schema_name)
        if not any(d['operator_id'] == message.from_user.id for d in dict_operators):
            message_from = message.from_user.full_name
            answer = await message.answer(emoji.emojize(':warning: ') +
                                          f'<code>{message_from}</code>, пожалуйста, пишите '
                                          f'сообщения в соответствии с правилами!')
            await database.add_service_message(schema_name, answer.message_id)
            await message.delete()
        else:
            pass
    else:
        pass
