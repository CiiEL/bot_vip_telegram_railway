from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
import os

BASE_PATH = "conteudo"
CHAT_ID_VIP = -4913959022

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = (
        f"Oi, {user.first_name} 😘\n\n"
        "Bem-vindo(a) ao *Clube VIP das Modelos* 🔥\n\n"
        "Aqui você tem acesso a fotos e vídeos exclusivos de várias modelos — tudo num único lugar!\n\n"
        "Digite: *quero vip* para liberar o acesso ou veja as modelos disponíveis 💋"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode="Markdown")

async def responder_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    print(f"[Recebido]: {texto}")

    if "quero vip" in texto or "acesso" in texto:
        await update.message.reply_text(
            "🔓 *Assinatura VIP - Acesso Completo*\n\n"
            "📸 Fotos e vídeos de TODAS as modelos\n"
            "💸 Apenas R$59,90 por mês\n\n"
            "Formas de pagamento:\n• Pix\n• Cartão\n• Boleto\n\n"
            "Digite: *pix* para receber a chave Pix",
            parse_mode="Markdown"
        )
    elif "pix" in texto:
        await update.message.reply_text(
            "💰 *Pagamento via Pix*\n\n"
            "Chave Pix: `vip@conteudo.com`\n"
            "Valor: R$59,90\n\n"
            "Envie o comprovante aqui mesmo após o pagamento 💋",
            parse_mode="Markdown"
        )
    elif "conteúdo" in texto or "modelos" in texto:
        await update.message.reply_text(
            "👑 *Modelos disponíveis:*\n\n"
            "• HannaOwO\n"
            "• Hazel Winters\n"
            "• Brida Nunes\n"
            "• Jean Grey Bianca\n"
            "• Brenda Trindade\n"
            "• Feer Campos\n"
            "• Giovana Genesini\n"
            "• Mari Reis\n"
            "• Thaissa Fit\n"
            "• Aline Farias\n"
            "• Debora Peixoto\n"
            "• Karol Rosalin\n"
            "• Renata Matos\n\n"
            "Tudo incluso na sua assinatura VIP 😍",
            parse_mode="Markdown"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="😅 Não entendi bem, mas se quiser o conteúdo VIP, digite *quero vip*.",
            parse_mode="Markdown"
        )

async def descobrir_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"O ID deste grupo é: {chat_id}")

async def liberar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Use: /liberar @usuario")
        return
    user_to_invite = context.args[0]
    try:
        link = await context.bot.create_chat_invite_link(
            chat_id=CHAT_ID_VIP,
            name=f"Acesso de {user_to_invite}",
            expire_date=datetime.utcnow() + timedelta(hours=24),
            member_limit=1
        )
        await update.message.reply_text(f"✅ Acesso liberado para {user_to_invite}:
{link.invite_link}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao gerar link: {e}")

async def acessar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    try:
        link = await context.bot.create_chat_invite_link(
            chat_id=CHAT_ID_VIP,
            name=f"Acesso de {nome}",
            expire_date=datetime.utcnow() + timedelta(hours=24),
            member_limit=1
        )
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎉 Olá {nome}! Aqui está seu link de acesso ao grupo VIP:
{link.invite_link}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Ocorreu um erro ao gerar seu acesso: {e}")