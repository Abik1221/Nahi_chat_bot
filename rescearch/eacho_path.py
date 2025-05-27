from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os
import logging

load_dotenv()
api_token = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=api_token)
dp = Dispatcher(bot)

# Dictionary of Latin Amharic to Feedel
latin_to_feedel = {
    "selam": "ሰላም",
    "endet": "እንዴት",
    "adrk": "አድርቅ",
    "dehna": "ደህና",
    "tena": "ጤና",
    "yene": "የኔ",
    "konjo": "ቆንጆ",
    "endemin": "እንደምን",
    "wedaj": "ወዳጅ",
    "ena": "እና",
    "ebakih": "እባክህ",
    "betam": "በጣም",
    "amesegenallo": "አመሰግናለሁ",
    "egziabher": "እግዚአብሔር"
    # Expand as needed
}

@dp.message_handler(commands=['start', 'help'])
async def command_start_handler(message: types.Message):
    await message.answer(
        "👋 Selam! I am **Auto_Replay** 🤖 — your Latin-to-Amharic word translator.\n"
        "Type something like: `selam endet adrk` and I’ll convert it into Feedel!\n\n"
        "🔤 Smart translation powered by Ethiopian Latin-Afaan mapping 🇪🇹"
    )

@dp.message_handler()
async def translate_message(message: types.Message):
    words = message.text.strip().lower().split()
    translated_words = [latin_to_feedel.get(word, word) for word in words]
    translated_sentence = ' '.join(translated_words)

    await message.reply(f"📝 {message.text} → {translated_sentence}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
