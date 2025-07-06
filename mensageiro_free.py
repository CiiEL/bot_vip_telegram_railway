from pathlib import Path
import random
import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()
TOKEN = os.getenv("TOKEN")
GRUPO_FREE_ID = int(os.getenv("GRUPO_FREE_ID"))

# Imagens hospedadas no Imgur
from imagens_free_links import MODELOS_IMAGENS

bot = Bot(token=TOKEN)

# Lista de modelos sem repetição
ordem_path = Path(".ordem_free.txt")
if not ordem_path.exists():
    ordem = list(MODELOS_IMAGENS.keys())
    random.shuffle(ordem)
    ordem_path.write_text("\n".join(ordem), encoding="utf-8")
else:
    ordem = ordem_path.read_text(encoding="utf-8").splitlines()

modelo = ordem.pop(0)
ordem.append(modelo)
ordem_path.write_text("\n".join(ordem), encoding="utf-8")

mensagem = (
    f"🔥 Conheça o conteúdo de *{modelo}*!\n\n"
    "💋 Esse é só um gostinho do que você encontra no nosso grupo VIP!\n"
    "Aproveite e veja o que temos disponível.\n\n"
    "_Tem mais alguma que te interessa? Sugira! Aceitamos pedidos para o próximo post!_"
)

imagens = MODELOS_IMAGENS.get(modelo, [])

async def enviar_mensagem_com_imagens():
    await bot.send_message(chat_id=GRUPO_FREE_ID, text=mensagem, parse_mode="Markdown")
    await asyncio.sleep(2)
    for url in imagens:
        await bot.send_photo(chat_id=GRUPO_FREE_ID, photo=url)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(enviar_mensagem_com_imagens())
