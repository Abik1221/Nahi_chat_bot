from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import os
import logging
from huggingface_hub import InferenceClient
from aiogram import executor


# Load environment variables
load_dotenv()
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
hf_token = os.getenv("HF_API_TOKEN")

# Logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=telegram_bot_token)
dp = Dispatcher(bot)

# Initialize Hugging Face client
hf_client = InferenceClient(token=hf_token)

# Class to store chat history
class Reference:
    def __init__(self):
        self.history = ""

reference = Reference()

# /start and /help commands
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Hello! I'm a chatbot created by your friend Nahom.\n"
        "Type any question, and I’ll try to help you.\n"
        "Use /clear_past to reset the chat memory."
    )

# /clear_past command
@dp.message_handler(commands=['clear_past'])
async def clear_history(message: types.Message):
    reference.history = ""
    await message.reply("✅ Chat memory cleared.")

# Main message handler
@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text
    prompt = f"{reference.history}\nUser: {user_input}\nAI:"

    try:
        result = hf_client.text_generation(
            prompt=prompt,
            model="tiiuae/falcon-7b-instruct",  # Open-access Hugging Face model
            max_new_tokens=100,
            temperature=0.7
        )

        bot_reply = result.strip()
        reference.history += f"\nUser: {user_input}\nAI: {bot_reply}"
        await bot.send_message(chat_id=message.chat.id, text=bot_reply)

    except Exception as e:
        logging.exception("Hugging Face request failed")
        await bot.send_message(chat_id=message.chat.id, text=f"❌ Error: {str(e)}")

# Run the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
