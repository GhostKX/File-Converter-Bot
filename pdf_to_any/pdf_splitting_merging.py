import buttons as bt
from user_states import UserFlow
import common_funtions as cf

from aiogram import F, Router
from aiogram.types import Message, FSInputFile, ContentType
from aiogram.fsm.context import FSMContext

import os
from PyPDF2 import PdfReader, PdfWriter


pdf_splitting_merging_router = Router()

######################################## ***** PDF File splitting and merging ***** ####################################


########################################################################################################################
                                            # Splitting pdf file to two pdf files

@pdf_splitting_merging_router.message(F.text, UserFlow.pdf_splitting)
async def pdf_file_splitting(message: Message, state: FSMContext):
    user_id = message.from_user.id
    sending_key = f'pdf_file_{user_id}'
    file_path = f'./pdf_to_any/pdf_files/'
    pdf_file_path = await cf.getting_initial_file_path(state, sending_key, file_path, file_type='pdf')

    part1_pdf_file_path = f'./pdf_to_any/pdf_split_merge_files/user_{user_id}_part_1.pdf'
    part2_pdf_file_path = f'./pdf_to_any/pdf_split_merge_files/user_{user_id}_part_2.pdf'

    if message.text == '⏮️ Back':
        await cf.removing_only_initial_file(pdf_file_path)
        await message.answer(f'🔙 Getting back'
                             f'\n\nMain Menu', reply_markup=bt.start_bot_buttons)
        await state.set_state(UserFlow.file_type)

    else:
        if os.path.exists(pdf_file_path) and message.text.isdigit():
            try:
                reader = PdfReader(pdf_file_path)
                total_pages = len(reader.pages)

                if total_pages == 1:
                    await message.answer('☹️ Error, invalid number of pages 💬', reply_markup=bt.start_bot_buttons)
                    await state.set_state(UserFlow.file_type)
                    await message.answer('🙏 Please try another pdf file!')
                    await cf.removing_only_initial_file(pdf_file_path)
                    return

                page_number = message.text
                try:
                    page_number = int(page_number)
                    if not 1 < page_number <= total_pages:
                        await message.answer('❌ Error. Invalid page number'
                                             '\n\n🙏 Please try again', reply_markup=bt.back_button)
                        await state.set_state(UserFlow.pdf_splitting)
                        return

                    part1_writer = PdfWriter()
                    for page in range(page_number):
                        part1_writer.add_page(reader.pages[page])

                    with open(part1_pdf_file_path, 'wb') as part1_file:
                        part1_writer.write(part1_file)

                    part2_writer = PdfWriter()
                    for page in range(page_number, total_pages):
                        part2_writer.add_page(reader.pages[page])

                    with open(part2_pdf_file_path, 'wb') as part2_file:
                        part2_writer.write(part2_file)

                    if os.path.exists(pdf_file_path) and os.path.exists(part1_pdf_file_path) and os.path.exists(
                            part2_pdf_file_path):
                        part1_file = FSInputFile(part1_pdf_file_path)
                        part2_file = FSInputFile(part2_pdf_file_path)

                        await message.bot.send_document(user_id, part1_file, reply_markup=bt.start_bot_buttons)
                        await message.bot.send_document(user_id, part2_file, reply_markup=bt.start_bot_buttons)
                        await state.set_state(UserFlow.file_type)

                        os.remove(pdf_file_path)
                        os.remove(part1_pdf_file_path)
                        os.remove(part2_pdf_file_path)

                except Exception as e:
                    await message.answer('❌ Error. Invalid symbols 🤨'
                                         '\n\n🙏 Please type in page number to split 💬', reply_markup=bt.back_button)
                    await state.set_state(UserFlow.pdf_splitting)
                    print(e)

            except Exception as e:
                await message.answer('☹️ Error occured with reading pdf file 💬', reply_markup=bt.start_bot_buttons)
                await state.set_state(UserFlow.file_type)
                await message.answer('🙏 Please try again later!')
                print(e)
                await cf.removing_only_initial_file(pdf_file_path)
        else:
            await message.answer('❌ Error. Invalid symbols 🤨'
                                 '\n\n🙏 Please type in page number to split 💬', reply_markup=bt.back_button)
            await state.set_state(UserFlow.pdf_splitting)

########################################################################################################################
                                            # Handling pdf files to merge


@pdf_splitting_merging_router.message(F.content_type == ContentType.DOCUMENT, UserFlow.pdf_merging)
async def pdf_handling_merging_files(message: Message, state: FSMContext):
    user_id = message.from_user.id
    file = message.document
    file_size = file.file_size
    file_name = file.file_name
    file_id = file.file_id

    file_location = 'pdf_to_any/pdf_files'

    if file_size > 20 * 1024 * 1024:
        await message.answer("❌ Error: The file size exceeds the 20 MB limit for bots ☹️"
                             "\n\nPlease upload a smaller file 💬", reply_markup=bt.back_button)
        return

    if file_name.endswith('.pdf'):

        destination_path = await cf.creating_unique_file_name(user_id, file_location, file_type='pdf')

        await message.bot.download(file=file_id, destination=destination_path)
        await state.set_state(UserFlow.pdf_merging)
        await message.answer('😊 Great'
                             '\n\n🙏 Now:'
                             '\n\n 1.  You can send other pdf files to merge 💬'
                             '\n\n 2.  Or you can click merge button ⬇️', reply_markup=bt.pdf_merge_files)
    else:
        await message.answer('❌ Invalid file type 🙁'
                             '\n\nPlease send an appropriate file 💬', reply_markup=bt.pdf_merge_files)
        await state.set_state(UserFlow.pdf_merging)


########################################################################################################################
                                            # Merging pdf files to one pdf

@pdf_splitting_merging_router.message(F.text, UserFlow.pdf_merging)
async def pdf_merging_files(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text == '✅ Merge Files':

        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(base_dir, '../pdf_to_any/pdf_files')

        list_all_files = os.listdir(save_dir)
        file_names = [file_name for file_name in list_all_files if file_name.startswith(f'user_{user_id}_')]

        if len(file_names) <= 1:
            await message.answer('❌ Not enough files to merge. Please upload more PDFs.',
                                 reply_markup=bt.pdf_merge_files)
            await state.set_state(UserFlow.pdf_merging)
            return

        file_names.sort(key=lambda file_name: os.path.getmtime(os.path.join(save_dir, file_name)))

        edited_pdf_files_path = os.path.join(base_dir, '../pdf_to_any/pdf_split_merge_files')
        merged_pdf_file_path = os.path.join(edited_pdf_files_path, f'merged_{user_id}.pdf')

        with open(merged_pdf_file_path, 'wb') as merged_pdf_file:
            writer = PdfWriter()
            for file_name in file_names:
                file_path = os.path.join(save_dir, file_name)
                with open(file_path, 'rb') as pdf_file:
                    reader = PdfReader(pdf_file)
                    for page in reader.pages:
                        writer.add_page(page)
            writer.write(merged_pdf_file)

        if os.path.exists(merged_pdf_file_path):
            document_pdf = FSInputFile(merged_pdf_file_path)
            await message.bot.send_document(user_id, document_pdf, reply_markup=bt.start_bot_buttons)
            await state.set_state(UserFlow.file_type)

            os.remove(merged_pdf_file_path)
            for file_name in file_names:
                os.remove(os.path.join(save_dir, file_name))

    ####################################################################################################################
                                                # Handling Back button logic

    elif message.text == '⏮️ Back':

        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(base_dir, f'../pdf_to_any/pdf_files')

        list_all_files = os.listdir(save_dir)
        file_names = [file_name for file_name in list_all_files if file_name.startswith(f'user_{user_id}_')]

        for file in file_names:
            file_path = os.path.join(save_dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)

        await message.answer(f'🔙 Getting back'
                             f'\n\nMain Menu', reply_markup=bt.start_bot_buttons)
        await state.set_state(UserFlow.file_type)
    else:
        await message.answer('❌ Invalid symbols 🙁'
                             '\n\nPlease use buttons below 💬', reply_markup=bt.pdf_merge_files)
        await state.set_state(UserFlow.pdf_merging)


########################################################################################################################
                                                    # The End