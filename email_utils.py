import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def enviar_email_redefinicao(destinatario, token):
    remetente = os.environ.get("GMAIL_USUARIO")
    senha = os.environ.get("GMAIL_SENHA_APP")

    link = f"http://127.0.0.1:5001/redefinir-senha/{token}"

    corpo = f"Recebemos um pedido para redefinir sua senha. Clique no link para continuar:\n\n{link}\n\nSe você não pediu isso, ignore este e-mail."

    mensagem = MIMEText(corpo)
    mensagem["Subject"] = "Redefinição de senha — Mural ABM"
    mensagem["From"] = remetente
    mensagem["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, mensagem.as_string())