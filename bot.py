from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text

    await update.message.reply_text("⏳ Генерирую...")

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4.1",
            "input": f"Создай сцену для видео: {prompt}"
        }
    )

    data = response.json()

    try:
        text = data["output"][0]["content"][0]["text"]
    except:
        text = "Ошибка генерации"

    await update.message.reply_text(text)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()
