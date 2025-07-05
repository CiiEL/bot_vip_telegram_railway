from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from handlers import start, responder_mensagem, descobrir_chat_id, liberar, acessar
from mensagens_free import mensagens_promocionais
from dotenv import load_dotenv
from telegram import Bot
import asyncio
import os
import random

load_dotenv()
TOKEN = os.getenv("TOKEN")
GRUPO_FREE_ID = int(os.getenv("GRUPO_FREE_ID"))
CHAT_ID_VIP = int(os.getenv("CHAT_ID_VIP")) 

# Agendador de mensagens automáticas no grupo FREE
async def enviar_mensagens_automaticas():
    bot = Bot(token=TOKEN)
    while True:
        mensagem = random.choice(mensagens_promocionais)
        await bot.send_message(chat_id=GRUPO_FREE_ID, text=mensagem, parse_mode="Markdown")
        await asyncio.sleep(60 * 60 * 3)  # a cada 3 horas

# Início da aplicação
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("idgrupo", descobrir_chat_id))
    app.add_handler(CommandHandler("liberar", liberar))
    app.add_handler(CommandHandler("acessar", acessar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensagem))

    print("🤖 Bot rodando...")
    await asyncio.gather(
        app.run_polling(),
        enviar_mensagens_automaticas()
    )

if __name__ == '__main__':
    asyncio.run(main())
