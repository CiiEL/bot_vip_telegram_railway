import asyncio
import random
from telegram import Bot
from mensagens_free import mensagens_promocionais
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
GRUPO_FREE_ID = int(os.getenv("GRUPO_FREE_ID"))
CHAT_ID_VIP = int(os.getenv("CHAT_ID_VIP"))

async def enviar_mensagens_automaticas():
    bot = Bot(token=TOKEN)
    while True:
        mensagem = random.choice(mensagens_promocionais)
        await bot.send_message(chat_id=GRUPO_FREE_ID, text=mensagem, parse_mode="Markdown")
        await asyncio.sleep(60 * 60 * 3)  # a cada 3 horas = 5x ao dia
