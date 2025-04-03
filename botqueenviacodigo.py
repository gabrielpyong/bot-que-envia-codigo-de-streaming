import imaplib
import email
import re
from html import unescape
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Configurações
EMAIL = "COLOQUE O SEU EMAIL AQUI"
SENHA = "SENHA DO EMAIL"
TOKEN_BOT = "TOKEN DO BOT AQUI"
CHAT_ID = "ID DO CHAT AQUI"

# Mapeamento de serviços para remetentes e assuntos
SERVICOS = {
    "Disney": {
        "email": "disneyplus@trx.mail2.disneyplus.com",
        "subject": "Seu código de acesso único para o Disney+"
    },
    "Prime": {
        "email": "account-update@amazon.com",
        "subject": None
    }
}

def get_latest_code(service_config):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(EMAIL, SENHA)
        mail.select("inbox")
        search_query = f'FROM "{service_config["email"]}"'
        _, data = mail.search(None, search_query)
        if not data[0]:
            mail.select("[Gmail]/Todos os e-mails", readonly=True)
            _, data = mail.search(None, search_query)
            if not data[0]:
                return "Nenhum e-mail encontrado", None
        
        # Garante que o bot pegue o e-mail mais recente
        latest_email_id = data[0].split()[-1]
        _, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        # Decodifica o assunto manualmente
        subject = msg["subject"]
        if subject:
            decoded_subject = email.header.decode_header(subject)[0][0]
            if isinstance(decoded_subject, bytes):
                subject = decoded_subject.decode("utf-8", errors="replace")
            print(f"Assunto do e-mail: {subject}")
        print(f"Data do e-mail: {msg['date']}")
        
        # Extrai o corpo do e-mail
        body = ""
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                print(f"Corpo texto simples: {body}")
            elif content_type == "text/html":
                html_body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                print(f"Corpo HTML completo: {html_body}")
                # Converte HTML para texto simples
                body = unescape(html_body).replace("<br>", "\n").replace("</p>", "\n").replace(" ", " ").replace("\t", " ")
                # Remove tags HTML simples para melhorar a extração
                body = re.sub(r"<[^>]+>", " ", body).strip()
        
        if not body:
            return "Corpo do e-mail não encontrado", None
        
        print(f"Texto extraído completo: {body}")
        
        # Lógica de extração baseada no serviço
        if service_config["email"] == "disneyplus@trx.mail2.disneyplus.com":
            # Para Disney
            code_match = re.search(r"(MyDisney|expira em 15 minutos)[\s\S]*?(\d{6})", body, re.IGNORECASE)
            if code_match and code_match.group(2):
                return code_match.group(2), body
        elif service_config["email"] == "account-update@amazon.com":
            # Para Amazon Prime, procura "seu código de verificação é:" seguido de 6 dígitos
            code_match = re.search(r"seu código de verificação é:[\s\S]*?(\d{6})", body, re.IGNORECASE)
            if code_match and code_match.group(1):
                return code_match.group(1), body
        
        # fallback para buscar qualquer 6 dígitos no texto (para depuração)
        code = re.search(r"\d{6}", body)
        if code:
            print(f"Código encontrado (fallback): {code.group()}")
            return code.group(), body
        return "Código não encontrado", body
    except Exception as e:
        print(f"Erro ao buscar e-mail: {e}")
        return f"Erro: {str(e)}", None
    finally:
        mail.logout()

async def codigo(update, context):
    # botões interativos
    keyboard = [
        [
            InlineKeyboardButton("Disney", callback_data="disney"),
            InlineKeyboardButton("Prime", callback_data="prime"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # mensagem com os botões
    await update.message.reply_text("Escolha o serviço de streaming:", reply_markup=reply_markup)

async def button_callback(update, context):
    query = update.callback_query
    await query.answer()  # Confirma que o clique foi recebido
    
    service = query.data  # Pega o callback_data (disney ou prime)
    service_map = {"disney": "Disney", "prime": "Prime"}
    
    if service in service_map:
        code, email_content = get_latest_code(SERVICOS[service_map[service]])
        if code and "Código não encontrado" not in code:
            await query.message.reply_text(f"Código {service_map[service]}: {code}")
        else:
            # Forçar codificação UTF-8 dps que enviar ao Telegram
            if email_content:
                email_content = email_content.encode('utf-8', errors='replace').decode('utf-8')
            await query.message.reply_text(f"{code}\n\nConteúdo do e-mail:\n{email_content[:4000]}")
    else:
        await query.message.reply_text("Serviço inválido. Use: Disney ou Prime")

def main():
    application = Application.builder().token(TOKEN_BOT).build()
    application.add_handler(CommandHandler("codigo", codigo))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.run_polling()

if __name__ == "__main__":
    main()