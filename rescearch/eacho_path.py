from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os 
import logging

load_dotenv()
api_token = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=api_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start','help'])
async def command_start_handler(message: types.Message):
    await message.answer("Hello! \n I Just developed by that stupid Nahom keneni, \n your besttttt, annoying and lovely friend. \n How can I assist you today?")
    

    
    
@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(message.text)
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)