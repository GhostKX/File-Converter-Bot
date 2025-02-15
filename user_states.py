from aiogram.fsm.state import State, StatesGroup


class UserFlow(StatesGroup):
    start = State()
    file_type = State()
    waiting_for_file = State()

    txt_converting_file_type = State()
    docx_converting_file_type = State()
    pdf_converting_file_type = State()

    pdf_splitting = State()
    pdf_merging = State()