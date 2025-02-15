from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_bot_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📄 TXT File"), KeyboardButton(text="📝 Word Docx"), KeyboardButton(text="📖 PDF Document")]
    ],
    resize_keyboard=True
)

back_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='⏮️ Back')]
    ],
    resize_keyboard=True
)

txt_convert_to = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 To Word Docx"), KeyboardButton(text="📖 To PDF Document"), KeyboardButton(text="📊 To PPT Presentation")],
        [KeyboardButton(text="📈 To Excel Spreadsheet"), KeyboardButton(text="🧾 To CSV File")],
        [KeyboardButton(text='⏮️ Back')]
    ],
    resize_keyboard=True
)


docx_convert_to = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 To TXT File"), KeyboardButton(text="📖 To PDF Document"), KeyboardButton(text="📊 To PPT Presentation")],
        [KeyboardButton(text='⏮️ Back')]
    ],
    resize_keyboard=True
)


pdf_convert_to = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🗂️ Split PDF File"), KeyboardButton(text="🗃️ Merge PDF Files")],
        [KeyboardButton(text="📄 To TXT File"), KeyboardButton(text="📝 To Word Docx"), KeyboardButton(text="📊 To PPT Presentation")],
        [KeyboardButton(text="📈 To Excel Spreadsheet"), KeyboardButton(text="🧾 To CSV File")],
        [KeyboardButton(text='⏮️ Back')]
    ],
    resize_keyboard=True
)


pdf_merge_files = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='✅ Merge Files'), KeyboardButton(text='⏮️ Back')]
    ],
    resize_keyboard=True
)