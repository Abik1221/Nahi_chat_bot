from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os 
import logging
from huggingface_hub import InferenceClient

load_dotenv()
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
api_token = os.getenv("HF_API_TOKEN")


hub_client = InferenceClient(token=api_token)

print("ok")