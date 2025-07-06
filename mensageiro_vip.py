import os
import asyncio
import random
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID_VIP = int(os.getenv("CHAT_ID_VIP"))
CAMINHO_VIP = "conteudo/vip"

bot = Bot(token=TOKEN)

mensagens_chamada = [
    "😈 Conteúdo quente no ar! Se liga nessa sequência...",
    "💋 As modelos mandaram ver hoje... dá uma olhada:",
    "🔥 Atualização VIP fresquinha só pros verdadeiros assinantes.",
    "📸 Curtiram o último drop? Esse aqui tá ainda melhor!",
    "🥵 Vem que essa sequência tá imperdível..."
]

def gerar_mensagem_vip():
    return random.choice(mensagens_chamada)

async def enviar_conteudo_vip():
    arquivos = os.listdir(CAMINHO_VIP)
    imagens = [a for a in arquivos if a.lower().endswith((".jpg", ".jpeg", ".png"))][:10]
    videos = [a for a in arquivos if a.lower().endswith((".mp4", ".mov", ".mkv"))][:5]

    if not imagens and not videos:
        print("Nenhum conteúdo encontrado para enviar.")
        return

    await bot.send_message(chat_id=CHAT_ID_VIP, text=gerar_mensagem_vip())

    for arquivo in imagens:
        caminho = os.path.join(CAMINHO_VIP, arquivo)
        with open(caminho, 'rb') as img:
            await bot.send_photo(chat_id=CHAT_ID_VIP, photo=img)
        await asyncio.sleep(15)

    for arquivo in videos:
        caminho = os.path.join(CAMINHO_VIP, arquivo)
        with open(caminho, 'rb') as vid:
            await bot.send_video(chat_id=CHAT_ID_VIP, video=vid)
        await asyncio.sleep(15)

async def executar_postagens():
    print("Enviando postagem VIP 1...")
    await enviar_conteudo_vip()
    await asyncio.sleep(900)  # 15 min = 900s

    print("Enviando postagem VIP 2...")
    await enviar_conteudo_vip()
    await asyncio.sleep(900)  # +15 min

    print("Enviando postagem VIP 3...")
    await enviar_conteudo_vip()

if __name__ == '__main__':
    asyncio.run(executar_postagens())
