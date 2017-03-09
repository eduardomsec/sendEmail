import mimetypes
import os
import smtplib

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def adiciona_anexo(msg, filename):
    if not os.path.isfile(filename):
        return

    ctype, encoding = mimetypes.guess_type(filename)

    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'

    maintype, subtype = ctype.split('/', 1)

    if maintype == 'text':
        with open(filename) as f:
            mime = MIMEText(f.read(), _subtype=subtype)
    elif maintype == 'image':
        with open(filename, 'rb') as f:
            mime = MIMEImage(f.read(), _subtype=subtype)
    elif maintype == 'audio':
        with open(filename, 'rb') as f:
            mime = MIMEAudio(f.read(), _subtype=subtype)
    else:
        with open(filename, 'rb') as f:
            mime = MIMEBase(maintype, subtype)
            mime.set_payload(f.read())

        encoders.encode_base64(mime)

    mime.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(mime)

user = input("User email: ")
passwod = input("Password email: ")
smtpMail = input("SMTP: ")
port = int(input("Port: "))
de = user
arq = input("Enter (email.txt) with list emails: ")
sub = input("Enter Subject: ")
attach = input("Enter Attachment: ") 
body = input("Body email: ")

for email in open(arq):
    msg = MIMEMultipart()
    msg['From'] = de
    #msg['To'] = ', '.join(para)
    msg['To'] = email
    msg['Subject'] = sub

    # Corpo da mensagem
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    # Arquivos anexos.
    # adiciona_anexo(msg, 'texto.txt')
    adiciona_anexo(msg, attach)

    raw = msg.as_string()
    smtp = smtplib.SMTP(smtpMail, port)
    smtp.starttls()
    smtp.login(user, passwod)
    print('Send - ' + email[:-1])
    smtp.sendmail(de, email[:-1], raw)
    smtp.quit()