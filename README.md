# Nahi Telegram Chatbot

A Telegram chatbot powered by Hugging Face's text-generation models via the Hugging Face Inference API.

---

## Features

- Receives messages from Telegram users.
- Sends the messages as prompts to Hugging Face's API for text generation.
- Returns generated responses back to Telegram users.
- Uses `aiogram` for Telegram bot integration.
- Uses `huggingface_hub` Python client to communicate with Hugging Face API.

---

## Prerequisites

- Python 3.8+
- Telegram Bot Token (from [BotFather](https://t.me/BotFather))
- Hugging Face API Token (from [Hugging Face Account](https://huggingface.co/settings/tokens))
- Basic familiarity with Python and terminal commands

---

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/Nahi_chat_bot.git
cd Nahi_chat_bot

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.\.venv\Scripts\activate       # Windows PowerShell

```bash
pip install -r requirements.txt

```bash
export TELEGRAM_API_TOKEN="your_telegram_token_here"
export HUGGINGFACE_API_TOKEN="your_huggingface_token_here"

Run the bot script:
```bash
python my_bot.py
