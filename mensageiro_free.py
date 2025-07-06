import asyncio
import random
import time
from telegram import Bot
from dotenv import load_dotenv
import os
from imagens_free_links import MODELOS_IMAGENS
from mensagens_free import mensagens_por_modelo

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID_FREE = int(os.getenv("GRUPO_FREE_ID"))

bot = Bot(token=TOKEN)

ordem_path = ".ordem_free.txt"

async def loop_envio_continuo():
    while True:
        # Lista de modelos sem repetição
        if not os.path.exists(ordem_path):
            ordem = list(MODELOS_IMAGENS.keys())
            random.shuffle(ordem)
            with open(ordem_path, "w", encoding="utf-8") as f:
                f.write("\n".join(ordem))
        else:
            with open(ordem_path, "r", encoding="utf-8") as f:
                ordem = f.read().splitlines()

        modelo = ordem.pop(0)
        ordem.append(modelo)

        with open(ordem_path, "w", encoding="utf-8") as f:
            f.write("\n".join(ordem))

        mensagem = mensagens_por_modelo.get(modelo, f"🔥 Conheça o conteúdo de *{modelo}*!\n\n💋 Esse é só um gostinho do que você encontra no nosso grupo VIP!")
        imagens = random.sample(MODELOS_IMAGENS.get(modelo, []), k=min(3, len(MODELOS_IMAGENS.get(modelo, []))))

        await bot.send_message(chat_id=CHAT_ID_FREE, text=mensagem, parse_mode="Markdown")
        await asyncio.sleep(2)
        for url in imagens:
            await bot.send_photo(chat_id=CHAT_ID_FREE, photo=url)
            await asyncio.sleep(5)

        print(f"[OK] Enviado: {modelo}")
        print("[INFO] Aguardando 45 minutos para o próximo envio...\n")
        await asyncio.sleep(2700)  # 45 minutos

if __name__ == "__main__":
    asyncio.run(loop_envio_continuo())
