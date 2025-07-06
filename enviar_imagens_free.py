import asyncio
import random
from telegram import Bot
from dotenv import load_dotenv
import os
from imagens_free_links import MODELOS_IMAGENS

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID_FREE = int(os.getenv("GRUPO_FREE_ID"))

bot = Bot(token=TOKEN)

def gerar_mensagem(modelo):
    return (
        "💋 Esse é só um gostinho do que você encontra no nosso grupo VIP!\n"
        "Aproveite e veja o que temos disponível.\n\n"
        "_Tem mais alguma que te interessa? Sugira! Aceitamos pedidos para o próximo post!_"
    )

async def enviar_imagens_free():
    for modelo, links in MODELOS_IMAGENS.items():
        imagens_escolhidas = random.sample(links, k=min(2, len(links)))
        
        mensagem = gerar_mensagem(modelo)
        await bot.send_message(chat_id=CHAT_ID_FREE, text=mensagem, parse_mode="Markdown")
        await asyncio.sleep(1)

        for url in imagens_escolhidas:
            await bot.send_photo(chat_id=CHAT_ID_FREE, photo=url)
            await asyncio.sleep(15)

        print(f"[OK] Enviado conteúdo da modelo: {modelo}")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(enviar_imagens_free())
