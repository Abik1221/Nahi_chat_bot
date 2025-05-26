import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from huggingface_hub import InferenceClient

# Enable logging
logging.basicConfig(level=logging.INFO)

# Your Telegram bot token
API_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Your Hugging Face API token
HF_API_TOKEN = "YOUR_HUGGINGFACE_API_TOKEN"

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Initialize Hugging Face Inference Client
hf_client = InferenceClient(token=HF_API_TOKEN)

# Simple conversation history (optional)
class Conversation:
    def __init__(self):
        self.history = ""

reference = Conversation()

@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text.strip()
    prompt = f"{reference.history}\nUser: {user_input}\nAI:"

    try:
        result = hf_client.text_generation(
            model="gpt2",          # You can change this to another supported model
            prompt=prompt,
            max_new_tokens=100,
            temperature=0.7,
        )
        bot_reply = result[0]["generated_text"].strip()

        # Update conversation history (optional, simple approach)
        reference.history += f"\nUser: {user_input}\nAI: {bot_reply}"

        await message.reply(bot_reply)

    except Exception as e:
        logging.exception("Hugging Face request failed")
        await message.reply(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    logging.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True)
