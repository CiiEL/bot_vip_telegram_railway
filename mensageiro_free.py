import asyncio
import random
import os
from datetime import datetime, time, timedelta
from telegram import Bot
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID_FREE = int(os.getenv("GRUPO_FREE_ID"))

modelos = [
    "HannaOwO", "Hazel Winters", "Brida Nunes", "Jean Grey Bianca", "Brenda Trindade",
    "Feer Campos", "Giovana Genesini", "Mari Reis", "Thaissa Fit", "Aline Farias",
    "Debora Peixoto", "Karol Rosalin", "Renata Matos"
]

bot = Bot(token=TOKEN)

# === MENSAGEM GERADA ===
def gerar_mensagem(hora, modelo):
    comum = (
        f"💋 Hoje é dia de *{modelo}* no nosso grupo!\n\n"
        "Conteúdo exclusivo no grupo VIP 🔥\n"
        "Assinatura: R$19,90/mês - Acesso completo!\n"
        "Pix: vip@conteudo.com\n\n"
        "Tem mais alguma que te interessa?\n"
        "Desfrute das que temos e sugira as que você gosta!\n"
        "Aceitamos pedidos para post! 💌"
    )

    especiais = {
        8: f"☀️ Bom dia, Clube das ++!\n\nComeçando a manhã com a maravilhosa *{modelo}* 😍\n\n",
        12: f"🍽️ Hora do almoço, mas também de aproveitar a *{modelo}*!\n\n",
        13: f"🥵 Já viu a *{modelo}* hoje? Se não, aproveita agora!\n\n",
        22: f"🌙 Fechando o dia com chave de ouro...\nHoje a estrela é *{modelo}* 💫\n\n"
    }

    return especiais.get(hora, "") + comum

# === AGENDA DE MENSAGENS ===
async def agendador():
    print("⏰ Agendador iniciado.")
    proxima = datetime.now().replace(minute=0, second=0, microsecond=0)

    if proxima.time() < time(8, 0):
        proxima = proxima.replace(hour=8)
    elif proxima.time() > time(22, 0):
        proxima = proxima.replace(hour=8) + timedelta(days=1)
    else:
        proxima += timedelta(hours=1)

    while True:
        agora = datetime.now()
        if agora >= proxima:
            modelo = random.choice(modelos)
            mensagem = gerar_mensagem(proxima.hour, modelo)

            try:
                await bot.send_message(chat_id=CHAT_ID_FREE, text=mensagem, parse_mode="Markdown")
                print(f"✅ Enviada às {proxima.hour}h: {modelo}")
            except Exception as e:
                print(f"❌ Erro ao enviar: {e}")

            # Define próximo horário
            proxima += timedelta(hours=1)
            if proxima.hour > 22:
                proxima = proxima.replace(hour=8) + timedelta(days=1)

        await asyncio.sleep(30)

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    asyncio.run(agendador())
