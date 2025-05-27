import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# --- Configuration ---
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
MODEL_NAME = "bigscience/bloomz-560m"

# --- Logging ---
logging.basicConfig(level=logging.INFO)

# --- Bot Initialization ---
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Transliteration Dictionary ---
translit_dict = {
    "selam": "ሰላም", "endet": "እንዴት", "adrk": "አድርክ", "neh": "ነህ", "nesh": "ነሽ",
    "dehna": "ደህና", "tena": "ጤና", "yistilign": "ይስጥልኝ", "betam": "በጣም",
    "amesegenallo": "አመሰግናለሁ"
}

# --- Load Model and Tokenizer ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)

# --- Transliteration Function ---
def transliterate_text(text: str) -> str:
    words = text.lower().split()
    transliterated = [translit_dict.get(word, word) for word in words]
    return " ".join(transliterated)

# --- Generate AI Reply Function ---
def generate_amharic_reply(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=40,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply.strip()

# --- Command Handlers ---
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.answer(
        "👋 Selam! I am Auto_Replay 🤖\nSpeak in Amharic or Latin-style Amharic — I'll understand and reply!\nTry saying: `selam endet adrk`"
    )

# --- Message Handler ---
@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text
    transliterated = transliterate_text(user_input)
    response = generate_amharic_reply(transliterated)
    await message.reply(response)

# --- Run the Bot ---
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
