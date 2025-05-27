from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
import os
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load environment variables
load_dotenv()
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Logging setup
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

# Load DialoGPT-small
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Store chat history per user
chat_history = {}

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("👋 Hello! I'm a chatbot powered by DialoGPT. Just message me anything!")

@dp.message_handler()
async def chat(message: types.Message):
    user_id = str(message.from_user.id)
    history = chat_history.get(user_id, None)

    # Encode user message
    new_input_ids = tokenizer.encode(message.text + tokenizer.eos_token, return_tensors='pt')

    # Combine with history if exists
    bot_input_ids = torch.cat([history, new_input_ids], dim=-1) if history is not None else new_input_ids

    # Generate response
    response_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Save new history
    chat_history[user_id] = bot_input_ids

    await message.reply(response)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
