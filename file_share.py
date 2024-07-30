import smtplib
import mimetypes
from email.message import EmailMessage

def mail_file(filepath,recipient="krishnanaravind8702@gmail.com"):
    message = EmailMessage()
    sender = "krishnanaravind8702@gmail.com"
    #recipient = "krishnanaravind8702@gmail.com"
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = 'Forensics Report'
    body = """PFA the results of the totaly exhaustive analysis of the suspect's emails"""
    message.set_content(body)
    mime_type, _ = mimetypes.guess_type(filepath)
    mime_type, mime_subtype = mime_type.split('/')
    with open(filepath, 'rb') as file:
        message.add_attachment(file.read(),
        maintype=mime_type,
        subtype=mime_subtype,
        filename=filepath[filepath.rfind("/")+1:])
    print(message)
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
    mail_server.set_debuglevel(1)
    mail_server.login("krishnanaravind8702@gmail.com", 'ditfficaavcppscl')
    mail_server.send_message(message)
    mail_server.quit()

#mail_file(f"/home/jfrans/Hackathon/Forensics/susygrime@gmail.com_metric.csv", "jfrancis4142@gmail.com")
