import os
from dotenv import load_dotenv
from datetime import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
import asyncio

# Carrega variáveis de ambiente
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID_VIP = int(os.getenv("CHAT_ID_VIP"))

# Caminho dos arquivos
CAMINHO_VIP = "conteudo/vip"

async def enviar_conteudo_vip():
    bot = Bot(token=TOKEN)

    if not os.path.exists(CAMINHO_VIP):
        print("❌ Pasta de conteúdo VIP não encontrada.")
        return

    arquivos = os.listdir(CAMINHO_VIP)
    fotos = [f for f in arquivos if f.lower().endswith((".jpg", ".jpeg", ".png"))][:10]
    videos = [f for f in arquivos if f.lower().endswith((".mp4", ".mov", ".avi"))][:5]

    for f in fotos:
        caminho = os.path.join(CAMINHO_VIP, f)
        with open(caminho, "rb") as img:
            await bot.send_photo(chat_id=CHAT_ID_VIP, photo=img)

    for v in videos:
        caminho = os.path.join(CAMINHO_VIP, v)
        with open(caminho, "rb") as vid:
            await bot.send_video(chat_id=CHAT_ID_VIP, video=vid)

    print("✅ Conteúdo VIP enviado com sucesso.")

def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(enviar_conteudo_vip, "cron", hour=10)
    scheduler.add_job(enviar_conteudo_vip, "cron", hour=15)
    scheduler.add_job(enviar_conteudo_vip, "cron", hour=21)
    scheduler.start()
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
