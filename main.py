import httpx

import asyncio
import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

# logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def get_usd_to_rub():
    ACCESS_KEY = os.environ.get('ACCESS_KEY')
    headers = {'apikey': ACCESS_KEY}

    URL = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1"
    async with httpx.AsyncClient() as client:
        r = await client.get(URL, headers=headers)
        usd_to_rub = r.json()
    return usd_to_rub['result']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    "Send a message when /start is issued"
    context.user_data['awaiting_name'] = True
    await update.message.reply_text(
        "Добрый день, как вас зовут?",
        reply_markup=ForceReply(selective=True),
    )


async def reset_name(update: Update,
                     context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['awaiting_name'] = False
    context.user_data['name'] = None
    await update.message.reply_text('Имя удаленно. Введите /start')


async def usd_to_rub_command(update: Update,
                             context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('awaiting_name'):
        context.user_data['awaiting_name'] = False
        name = update.message.text
        context.user_data['name'] = name
        result = await get_usd_to_rub()
        result = int(result)
        msg = f"Рад знакомству, {name}! Курс доллара сегодня {result}р."
        await update.message.reply_text(msg)
    elif context.user_data.get('name'):
        name = context.user_data.get('name')
        result = await get_usd_to_rub()
        result = int(result)
        msg = f"Рад знакомству, {name}! Курс доллара сегодня {result}р."
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text('Введите /start')


def main() -> None:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset_name", reset_name))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, usd_to_rub_command))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
