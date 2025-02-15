import buttons as bt
from user_states import UserFlow

import os
import uuid

from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart


file_type_handling_router = Router()


@file_type_handling_router.message(CommandStart())
async def start_bot(message: Message, state: FSMContext):
    await message.answer('✨ Welcome to the file converter bot! ✨'
                         '\n\nPlease choose type of file to work with', reply_markup=bt.start_bot_buttons)
    await state.set_state(UserFlow.file_type)


@file_type_handling_router.message(F.text.in_(['📄 TXT File', '📝 Word Docx', '📖 PDF Document',
                                               '📊 PPT Presentation', '📈 Excel Spreadsheet', '🧾 CSV File']),
                                   UserFlow.file_type)
async def handle_file_type(message: Message, state: FSMContext):
    file_type_name = message.text
    await state.update_data(selected_file_type=file_type_name)
    await message.answer(f'😊 Nice'
                         f'\n\n🙏 Now please send me your {file_type_name}', reply_markup=bt.back_button)
    await state.set_state(UserFlow.waiting_for_file)


@file_type_handling_router.message(UserFlow.file_type)
async def file_type_error_handler_for_text(message: Message, state: FSMContext):
    await message.answer('❌ Error. Invalid symbols 🤨'
                         '\n\nPlease use buttons below 💬', reply_markup=bt.start_bot_buttons)
    await state.set_state(UserFlow.file_type)


@file_type_handling_router.message(F.text == '⏮️ Back', UserFlow.waiting_for_file)
async def getting_back(message: Message, state: FSMContext):
    await message.answer(f'🔙 Getting back'
                         f'\n\nMain Menu', reply_markup=bt.start_bot_buttons)
    await state.set_state(UserFlow.file_type)


@file_type_handling_router.message(F.text, UserFlow.waiting_for_file)
async def file_type_error_handler(message: Message, state: FSMContext):
    await message.answer('❌ Error. Invalid symbols please use button below 🤨',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Or send appropriate file 💬', reply_markup=bt.back_button)
    await state.set_state(UserFlow.waiting_for_file)


@file_type_handling_router.message(F.content_type == ContentType.DOCUMENT, UserFlow.waiting_for_file)
async def file_handling(message: Message, state: FSMContext):
    user_id = message.from_user.id
    file = message.document
    file_size = file.file_size
    file_name = file.file_name
    file_id = file.file_id

    if file_size > 20 * 1024 * 1024:
        await message.answer("❌ Error: The file size exceeds the 20 MB limit for bots ☹️"
                             "\n\nPlease upload a smaller file 💬", reply_markup=bt.back_button)
        return

    file_type = await state.get_data()
    selected_file_type = file_type.get('selected_file_type')

    ####################################################################################################################
                                                # Handling TXT File

    if selected_file_type == '📄 TXT File' and file_name.endswith('.txt'):

        file_location = '../txt_to_any/txt_files'
        sending_key = f'txt_file_{user_id}'

        await saving_file(message, state, user_id, file_location, file_id, sending_key, file_type='txt')
        await state.set_state(UserFlow.txt_converting_file_type)
        await message.answer('😊 Great'
                             '\n\n🙏 Now please select file type to convert to 💬', reply_markup=bt.txt_convert_to)

    ####################################################################################################################
                                                # Handling DOCX File

    elif selected_file_type == '📝 Word Docx' and file_name.endswith('.docx'):

        file_location = '../docx_to_any/docx_files'
        sending_key = f'docx_file_{user_id}'

        await saving_file(message, state, user_id, file_location, file_id, sending_key, file_type='docx')
        await state.set_state(UserFlow.docx_converting_file_type)
        await message.answer('😊 Great'
                             '\n\n🙏 Now please select file type to convert to 💬', reply_markup=bt.docx_convert_to)

    ####################################################################################################################
                                                # Handling PDF File

    elif selected_file_type == '📖 PDF Document' and file_name.endswith('.pdf'):

        file_location = '../pdf_to_any/pdf_files'
        sending_key = f'pdf_file_{user_id}'

        await saving_file(message, state, user_id, file_location, file_id, sending_key, file_type='pdf')
        await state.set_state(UserFlow.pdf_converting_file_type)
        await message.answer('😊 Great'
                             '\n\n🙏 Now please select file type to convert to 💬', reply_markup=bt.pdf_convert_to)

    ####################################################################################################################
                                                # Handling else

    else:
        await message.answer('❌ Invalid file type 🙁'
                             '\n\nPlease send an appropriate file 💬', reply_markup=bt.back_button)
        await state.set_state(UserFlow.waiting_for_file)


########################################################################################################################
                                              # Other supportive functions

async def saving_file(message: Message, state: FSMContext, user_id, file_location, file_id, sending_key, file_type):

    unique_name = f'user_{user_id}_{uuid.uuid4()}'

    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, f'{file_location}')

    os.makedirs(save_dir, exist_ok=True)
    destination_path = os.path.join(save_dir, f'{unique_name}.{file_type}')

    await message.bot.download(file=file_id, destination=destination_path)
    await state.update_data({sending_key: unique_name})


########################################################################################################################
                                                         # The End