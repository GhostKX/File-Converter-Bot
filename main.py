from config import API_KEY
from txt_to_any.txt_to_any_conversion import txt_router
from docx_to_any.docx_to_any_conversion import docx_router
from pdf_to_any.pdf_to_any_conversion import pdf_router
from pdf_to_any.pdf_splitting_merging import pdf_splitting_merging_router
from start_bot_and_file_handling.PythonFileConverter_bot import file_type_handling_router
import asyncio
import logging

from aiogram import Bot, Dispatcher

bot_token = API_KEY

bot = Bot(token=bot_token)
dp = Dispatcher()


async def main():
    dp.include_router(file_type_handling_router)
    dp.include_router(txt_router)
    dp.include_router(docx_router)

    dp.include_router(pdf_router)
    dp.include_router(pdf_splitting_merging_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())