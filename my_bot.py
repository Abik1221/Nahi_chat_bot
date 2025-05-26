from aiogram import Bot, Dispatcher, types
from aiogram import executor
from dotenv import load_dotenv
import os
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load environment variables
load_dotenv()
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize Telegram bot
bot = Bot(token=telegram_bot_token)
dp = Dispatcher(bot)

# Initialize the model and tokenizer
model_name = "microsoft/DialoGPT-medium"  # Using medium instead of large for better performance
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Chat history management
class ChatHistory:
    def __init__(self):
        self.history = []
        self.max_history = 4  # Keep last 4 exchanges
    
    def add_exchange(self, user_input, bot_response):
        self.history.extend([user_input, bot_response])
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]
    
    def get_prompt(self, new_input):
        prompt = ""
        for i in range(0, len(self.history), 2):
            prompt += f"User: {self.history[i]}\nAI: {self.history[i+1]}\n"
        prompt += f"User: {new_input}\nAI:"
        return prompt
    
    def clear(self):
        self.history = []

chat_history = ChatHistory()

# Command handlers
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Hello! I'm your AI assistant.\n"
        "Just type your message and I'll respond.\n"
        "Use /clear to reset our conversation."
    )

@dp.message_handler(commands=['clear'])
async def clear_history(message: types.Message):
    chat_history.clear()
    await message.reply("✅ Conversation history cleared.")

# Message handler
@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        # Prepare the input
        prompt = chat_history.get_prompt(message.text)
        
        # Tokenize and generate response
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(
            inputs,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.9,
            temperature=0.7
        )
        
        # Decode and clean the response
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        bot_response = full_response[len(prompt):].strip()
        
        # Update history and send response
        chat_history.add_exchange(message.text, bot_response)
        await message.reply(bot_response)
    
    except Exception as e:
        logging.error(f"Error generating response: {str(e)}")
        await message.reply("❌ Sorry, I encountered an error. Please try again.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)