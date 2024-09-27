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
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    "Send a message when the command /help is issued"
    await update.message.reply_text("Help!")


async def usd_to_rub_command(update: Update,
                             context: ContextTypes.DEFAULT_TYPE) -> None:
    result = await get_usd_to_rub()
    result = round((result), 2)
    msg = f"1 USD = {result} RUB"
    await update.message.reply_text(msg)


def main() -> None:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, usd_to_rub_command))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

# async def f():
#     print('Start')
#     await asyncio.sleep(5)
#     print("sleep 5 ends")

# async def main():

#     task1 = asyncio.create_task(get_usd_to_rub())
#     task2 = asyncio.create_task(f())

#     result = asyncio.gather(task1, task2)
#     usd_to_rub = await result

#     print(usd_to_rub)

# asyncio.run(main())
