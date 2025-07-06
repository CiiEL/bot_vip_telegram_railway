from pathlib import Path
import shutil
import asyncio
from telegram import Bot
from telegram.request import HTTPXRequest
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID_VIP = int(os.getenv("CHAT_ID_VIP"))

request = HTTPXRequest(connect_timeout=30, read_timeout=60)
bot = Bot(token=TOKEN, request=request)

ENVIADAS_PATH = Path("conteudo/vip/.enviadas")
ENVIADAS_PATH.mkdir(parents=True, exist_ok=True)

def gerar_mensagem_vip(modelo):
    return (
        f"🔥 Conteúdo exclusivo da modelo *{modelo.replace('_', ' ').title()}*!\n\n"
        "💋 Fotos e vídeos íntimos disponíveis apenas no nosso clube VIP!\n\n"
        "_Tem mais alguma que te interessa? Sugira! Aceitamos pedidos para o próximo post!_"
    )

def listar_arquivos(modelo, tipo):
    pasta = Path(f"conteudo/vip/{modelo}")
    if not pasta.exists():
        return []
    if tipo == "imagem":
        return list(pasta.glob("*.jpg")) + list(pasta.glob("*.png")) + list(pasta.glob("*.jpeg"))
    elif tipo == "video":
        return list(pasta.glob("*.mp4")) + list(pasta.glob("*.mov"))
    return []

def mover_para_enviados(arquivo):
    destino = ENVIADAS_PATH / arquivo.name
    shutil.move(str(arquivo), destino)

async def enviar_conteudo_de_modelo(modelo):
    imagens = listar_arquivos(modelo, "imagem")[:10]
    videos = listar_arquivos(modelo, "video")[:5]

    if not imagens and not videos:
        print(f"[AVISO] Pasta da modelo '{modelo}' está vazia.")
        return

    legenda = gerar_mensagem_vip(modelo)
    await bot.send_message(chat_id=CHAT_ID_VIP, text=legenda, parse_mode="Markdown")

    for img in imagens:
        try:
            with open(img, "rb") as photo:
                await bot.send_photo(chat_id=CHAT_ID_VIP, photo=photo)
            mover_para_enviados(img)
            await asyncio.sleep(15)
        except Exception as e:
            print(f"[Erro ao enviar imagem {img.name}]: {e}")

    for vid in videos:
        try:
            with open(vid, "rb") as video:
                await bot.send_video(chat_id=CHAT_ID_VIP, video=video)
            mover_para_enviados(vid)
            await asyncio.sleep(15)
        except Exception as e:
            print(f"[Erro ao enviar vídeo {vid.name}]: {e}")

async def main():
    modelos = [  "giovana_genesini"]
    for modelo in modelos:
        await enviar_conteudo_de_modelo(modelo)

if __name__ == "__main__":
    asyncio.run(main())
