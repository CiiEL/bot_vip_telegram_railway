from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, responder_mensagem, descobrir_chat_id, liberar, acessar
import os

TOKEN = os.getenv("TOKEN")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("idgrupo", descobrir_chat_id))
    app.add_handler(CommandHandler("liberar", liberar))
    app.add_handler(CommandHandler("acessar", acessar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensagem))
    print("🤖 Bot rodando...")
    app.run_polling()