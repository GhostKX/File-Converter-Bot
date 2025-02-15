import buttons as bt
from user_states import UserFlow

import os
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

import uuid


async def sending_converted_file(message: Message, state: FSMContext, user_id, initial_file_path, converted_file_path):
    if os.path.exists(initial_file_path) and os.path.exists(converted_file_path):
        document_file = FSInputFile(converted_file_path)

        await message.bot.send_document(user_id, document_file, reply_markup=bt.start_bot_buttons)
        await state.set_state(UserFlow.file_type)

        os.remove(initial_file_path)
        os.remove(converted_file_path)


async def getting_initial_file_path(state: FSMContext, sending_key, file_path, file_type):
    initial_file_name = await state.get_data()
    initial_file_name = initial_file_name.get(sending_key)
    initial_file_path = f'{file_path}{initial_file_name}.{file_type}'
    return initial_file_path


async def creating_unique_file_name(user_id, file_location, file_type):
    unique_name = f'user_{user_id}_{uuid.uuid4()}'

    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, f'{file_location}')
    os.makedirs(save_dir, exist_ok=True)
    destination_path = os.path.join(save_dir, f'{unique_name}.{file_type}')
    return destination_path


async def removing_only_initial_file(initial_file_path):
    if os.path.exists(initial_file_path):
        os.remove(initial_file_path)
