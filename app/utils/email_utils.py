import smtplib
from email.message import EmailMessage
from flask import current_app


def send_email(destinatario: str, assunto: str, corpo_html: str, corpo_texto: str = None):
    cfg = current_app.config
    server = cfg.get('MAIL_SERVER')
    port = cfg.get('MAIL_PORT')
    username = cfg.get('MAIL_USERNAME')
    password = cfg.get('MAIL_PASSWORD')
    use_tls = cfg.get('MAIL_USE_TLS', True)
    use_ssl = cfg.get('MAIL_USE_SSL', False)
    default_sender = cfg.get('MAIL_DEFAULT_SENDER') or username

    if not server or not port or not username or not password:
        raise RuntimeError('Configuração SMTP incompleta. Defina MAIL_SERVER, MAIL_PORT, MAIL_USERNAME e MAIL_PASSWORD nas variáveis de ambiente.')

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = default_sender
    msg['To'] = destinatario
    if corpo_texto:
        msg.set_content(corpo_texto)
    msg.add_alternative(corpo_html, subtype='html')

    if use_ssl:
        smtp = smtplib.SMTP_SSL(server, port)
    else:
        smtp = smtplib.SMTP(server, port)
    try:
        smtp.ehlo()
        if use_tls and not use_ssl:
            smtp.starttls()
            smtp.ehlo()
        smtp.login(username, password)
        smtp.send_message(msg)
    finally:
        smtp.quit()
