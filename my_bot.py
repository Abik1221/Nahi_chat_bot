import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from traceback import format_exc

# Load .env file
load_dotenv()

# Tokens from environment
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Logging
logging.basicConfig(level=logging.INFO)

# Hugging Face and Telegram bot setup
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
hf_client = InferenceClient(token=HF_API_TOKEN)

# Conversation state
class ChatHistory:
    def __init__(self):
        self.history = []

    def reset(self):
        self.history = []

    def add_user(self, msg):
        self.history.append(f"User: {msg}")

    def add_bot(self, msg):
        self.history.append(f"Assistant: {msg}")

    def get_prompt(self):
        return "\n".join(self.history) + "\nAssistant:"

chat = ChatHistory()

# Handle /start and /help
@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    chat.reset()
    await message.reply(
        "👋 Hello! I'm Nahi_Bot, created by your friend Nahom.\n"
        "Just send me a message and I’ll try to help.\n"
        "Use /clear_past to reset the chat memory."
    )

# Handle /clear_past
@dp.message_handler(commands=["clear_past"])
async def clear(message: types.Message):
    chat.reset()
    await message.reply("✅ Chat memory cleared.")

# Handle user messages
@dp.message_handler()
async def main_bot(message: types.Message):
    try:
        user_input = message.text
        chat.add_user(user_input)
        prompt = chat.get_prompt()

        # Call DeepSeek model using text generation
        response = hf_client.text_generation(
            model="tiiuae/falcon-7b-instruct",
            prompt=prompt,
            max_new_tokens=200,
            temperature=0.7,
            stop=["User:", "Assistant:"]
        )

        # Extract assistant's reply
        answer = response.generated_text.replace(prompt, "").strip()
        chat.add_bot(answer)

        await bot.send_message(chat_id=message.chat.id, text=answer)

    except Exception as e:
        error_details = format_exc()
        print(f"❌ Exception occurred:\n{error_details}")
        await bot.send_message(chat_id=message.chat.id, text="❌ Error: Something went wrong. Please try again.")

# Run the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
