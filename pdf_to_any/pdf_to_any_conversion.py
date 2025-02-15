import buttons as bt
from user_states import UserFlow
import common_funtions as cf

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import pandas as pd
import pdfplumber
from pdf2docx import Converter
import subprocess
import csv

pdf_router = Router()

################################## ***** PDF converting to TXT, DOCX, PPT, CSV, XLSX ***** #############################


@pdf_router.message(F.text, UserFlow.pdf_converting_file_type)
async def pdf_file_converting_to(message: Message, state: FSMContext):
    user_id = message.from_user.id
    sending_key = f'pdf_file_{user_id}'
    file_path = f'./pdf_to_any/pdf_files/'

    pdf_file_path = await cf.getting_initial_file_path(state, sending_key, file_path, file_type='pdf')

    converted_file_location = 'pdf_to_any/pdf_converted_files'

    ####################################################################################################################
                            # Splitting pdf file into two parts, logic is in separate file

    if message.text == '🗂️ Split PDF File':
        await state.set_state(UserFlow.pdf_splitting)
        await message.answer('😊 Great'
                             '\n\n🙏 Please type in page number to split 💬', reply_markup=bt.back_button)

    ####################################################################################################################
                                # Merging pdf files into one, logic is in separate file

    elif message.text == '🗃️ Merge PDF Files':
        await state.set_state(UserFlow.pdf_merging)
        await message.answer('😊 Great'
                             '\n\n🙏 Please send other pdf files to merge 💬', reply_markup=bt.pdf_merge_files)

    ####################################################################################################################
                                            # PDF file converting to CSV

    elif message.text == '📄 To TXT File':
        converted_file_path = await cf.creating_unique_file_name(user_id, converted_file_location, file_type='txt')

        with pdfplumber.open(pdf_file_path) as pdf_file, open(converted_file_path, 'w', encoding='utf-8') as txt_file:
            for page in pdf_file.pages:
                text = page.extract_text()
                if text:
                    txt_file.write(page.extract_text() + '\n\n\n')

        await cf.sending_converted_file(message, state, user_id, pdf_file_path, converted_file_path)

    ####################################################################################################################
                                            # PDF File converting to DOCX

    elif message.text == '📝 To Word Docx':

        converted_file_path = await cf.creating_unique_file_name(user_id, converted_file_location, file_type='docx')

        cv = Converter(pdf_file_path)
        cv.convert(converted_file_path)
        cv.close()

        await cf.sending_converted_file(message, state, user_id, pdf_file_path, converted_file_path)

    ####################################################################################################################
                                            # PDF File converting to PPT

    elif message.text == '📊 To PPT Presentation':

        converted_file_path = await cf.creating_unique_file_name(user_id, converted_file_location, file_type='pptx')

        subprocess.run(['pdf2pptx', pdf_file_path, f'-o{converted_file_path}'])

        await cf.sending_converted_file(message, state, user_id, pdf_file_path, converted_file_path)

    ####################################################################################################################
                                            # PDF file converting to CSV

    elif message.text == '🧾 To CSV File':

        converted_file_path = await cf.creating_unique_file_name(user_id, converted_file_location, file_type='csv')

        with pdfplumber.open(pdf_file_path) as pdf_file:
            with open(converted_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                for page_number, page in enumerate(pdf_file.pages, start=1):
                    table = page.extract_table()
                    if table:
                        writer.writerow([f'Page {page_number} Table:'])
                        for row in table:
                            writer.writerows([row])
                        writer.writerow([])
                    else:
                        text = page.extract_text()
                        if text:
                            writer.writerow([f'Page {page_number} Text:'])
                            paragraphs = text.split("\n\n")
                            for paragraph in paragraphs:
                                if paragraph.strip():
                                    writer.writerow([paragraph.strip()])
                            writer.writerow([])

        await cf.sending_converted_file(message, state, user_id, pdf_file_path, converted_file_path)

    ####################################################################################################################
                                            # PDF File converting to XLSX

    elif message.text == '📈 To Excel Spreadsheet':

        converted_file_path = await cf.creating_unique_file_name(user_id, converted_file_location, file_type='xlsx')

        text_data = []

        with pdfplumber.open(pdf_file_path) as pdf_file:
            for page_number, page in enumerate(pdf_file.pages, start=1):
                table = page.extract_table()
                if table:
                    for row in table:
                        text_data.append(row)
                else:
                    text = page.extract_text()
                    if text:
                        paragraphs = text.split('\n')
                        for paragraph in paragraphs:
                            if paragraph.strip():
                                text_data.append([paragraph.strip()])

        df = pd.DataFrame(text_data)
        df.to_excel(converted_file_path, index=False)

        await cf.sending_converted_file(message, state, user_id, pdf_file_path, converted_file_path)

    ####################################################################################################################
                                            # Handling Back button logic

    elif message.text == '⏮️ Back':
        await cf.removing_only_initial_file(pdf_file_path)
        await message.answer(f'🔙 Getting back'
                             f'\n\nMain Menu', reply_markup=bt.start_bot_buttons)
        await state.set_state(UserFlow.file_type)

    else:
        await message.answer('❌ Error. Invalid symbols 🤨'
                             '\n\n🙏 Please use buttons below 💬', reply_markup=bt.pdf_convert_to)
        await state.set_state(UserFlow.pdf_converting_file_type)


########################################################################################################################
                                                    # The End
