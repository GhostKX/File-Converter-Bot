import buttons as bt
from user_states import UserFlow
import common_funtions as cf

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import os
from docx import Document
from docx2pdf import convert
import subprocess


docx_router = Router()

######################################## ***** DOCX converting to TXT, PDF, PPT ***** ##################################


@docx_router.message(F.text, UserFlow.docx_converting_file_type)
async def docx_file_converting_to(message: Message, state: FSMContext):
    user_id = message.from_user.id
    sending_key = f'docx_file_{user_id}'
    file_path = f'./docx_to_any/docx_files/'
    docx_file_path = await cf.getting_initial_file_path(state, sending_key, file_path, file_type='docx')

    converted_file_path = f'docx_to_any/docx_converted_files'

    ####################################################################################################################
                                                # Docx File converting to TXT

    if message.text == "📝 To TXT File":
        txt_file_path = await cf.creating_unique_file_name(user_id, converted_file_path, file_type='txt')
        document = Document(docx_file_path)

        with open(txt_file_path, 'w', encoding='UTF-8') as txt_file:
            for paragraph in document.paragraphs:
                txt_file.write(paragraph.text + '\n')

        await cf.sending_converted_file(message, state, user_id, docx_file_path, txt_file_path)

    ####################################################################################################################
                                                # Docx File converting to PDF

    elif message.text == "📖 To PDF Document":
        pdf_file_path = await cf.creating_unique_file_name(user_id, converted_file_path, file_type='pdf')

        if os.path.exists(docx_file_path):
            print(docx_file_path)
            print(pdf_file_path)
            convert(docx_file_path, pdf_file_path)
            await cf.sending_converted_file(message, state, user_id, docx_file_path, pdf_file_path)

    ####################################################################################################################
                                             # Docx File converting to PPT

    elif message.text == '📊 To PPT Presentation':

        pdf_file_path = await cf.creating_unique_file_name(user_id, converted_file_path, file_type='pdf')
        pptx_file_path = await cf.creating_unique_file_name(user_id, converted_file_path, file_type='pptx')

        if os.path.exists(docx_file_path):
            convert(docx_file_path, pdf_file_path)
            subprocess.run(['pdf2pptx', pdf_file_path, f'-o{pptx_file_path}'])

            if os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)

            await cf.sending_converted_file(message, state, user_id, docx_file_path, pptx_file_path)

    ####################################################################################################################
                                                # Handling Back button logic

    elif message.text == '⏮️ Back':
        await cf.removing_only_initial_file(docx_file_path)
        await message.answer(f'🔙 Getting back'
                             f'\n\nMain Menu', reply_markup=bt.start_bot_buttons)
        await state.set_state(UserFlow.file_type)

    else:
        await message.answer('❌ Error. Invalid symbols please use buttons below 🤨', reply_markup=bt.docx_convert_to)
        await state.set_state(UserFlow.docx_converting_file_type)


########################################################################################################################
                                                        # The End