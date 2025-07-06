from pathlib import Path
import random
import shutil
import time
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID_VIP = int(os.getenv("CHAT_ID_VIP"))

# Nomes corretos das pastas (minúsculo e underscore)
MODELOS = [
    "hannaowo", "hazel_winters", "brida_nunes", "jean_grey_bianca",
    "brenda_trindade", "feer_campos", "giovana_genesini", "mari_reis",
    "thaissa_fit", "aline_farias", "debora_peixoto", "karol_rosalin", "renata_matos"
]

# Nomes bonitos para exibição nas mensagens
NOMES_MODELOS = {
    "hannaowo": "HannaOwO",
    "hazel_winters": "Hazel Winters",
    "brida_nunes": "Brida Nunes",
    "jean_grey_bianca": "Jean Grey Bianca",
    "brenda_trindade": "Brenda Trindade",
    "feer_campos": "Feer Campos",
    "giovana_genesini": "Giovana Genesini",
    "mari_reis": "Mari Reis",
    "thaissa_fit": "Thaissa Fit",
    "aline_farias": "Aline Farias",
    "debora_peixoto": "Debora Peixoto",
    "karol_rosalin": "Karol Rosalin",
    "renata_matos": "Renata Matos"
}

ENVIADAS_PATH = Path("conteudo/vip/.enviadas")
ENVIADAS_PATH.mkdir(parents=True, exist_ok=True)
bot = Bot(token=TOKEN)

def gerar_mensagem_vip(modelo):
    nome_bonito = NOMES_MODELOS.get(modelo, modelo)
    return (
        f"🔥 Conteúdo exclusivo da modelo *{nome_bonito}*!\n\n"
        "💋 Fotos e vídeos íntimos disponíveis apenas no nosso clube VIP!\n\n"
        "_Tem mais alguma que te interessa? Sugira! Aceitamos pedidos para o próximo post!_"
    )

def carregar_ordem_modelos():
    ordem_path = ENVIADAS_PATH / "ordem.txt"
    if ordem_path.exists():
        with open(ordem_path, "r") as f:
            ordem = f.read().splitlines()
    else:
        ordem = random.sample(MODELOS, len(MODELOS))
        with open(ordem_path, "w") as f:
            f.write("\n".join(ordem))
    return ordem

def salvar_ordem_modelos(ordem):
    with open(ENVIADAS_PATH / "ordem.txt", "w") as f:
        f.write("\n".join(ordem))

def escolher_proxima_modelo():
    ordem = carregar_ordem_modelos()
    if not ordem:
        ordem = random.sample(MODELOS, len(MODELOS))
    modelo = ordem.pop(0)
    salvar_ordem_modelos(ordem + [modelo])
    return modelo

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

async def enviar_conteudo_vip():
    modelo = escolher_proxima_modelo()
    imagens = listar_arquivos(modelo, "imagem")[:10]
    videos = listar_arquivos(modelo, "video")[:5]

    if not imagens and not videos:
        print(f"[AVISO] Pasta da modelo '{modelo}' está vazia. Pulando envio.")
        return

    legenda = gerar_mensagem_vip(modelo)
    await bot.send_message(chat_id=CHAT_ID_VIP, text=legenda, parse_mode="Markdown")

    for img in imagens:
        with open(img, "rb") as photo:
            await bot.send_photo(chat_id=CHAT_ID_VIP, photo=photo)
        mover_para_enviados(img)
        time.sleep(15)

    for vid in videos:
        with open(vid, "rb") as video:
            await bot.send_video(chat_id=CHAT_ID_VIP, video=video)
        mover_para_enviados(vid)
        time.sleep(15)
