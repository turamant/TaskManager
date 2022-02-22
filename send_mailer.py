import os
import smtplib

from dotenv import load_dotenv


def send_email(body_text):
    """
    Send an email
    """
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    host = os.environ.get("SERVER")
    from_addr = os.environ.get("FROM_ADDR")
    to_addr = os.environ.get("TO_ADDR")
    subject = os.environ.get("SUBJECT")
    if host and from_addr and to_addr and subject:
        BODY = "\r\n".join((
            "From: %s" % from_addr,
            "To: %s" % to_addr,
            "Subject: %s" % subject,
            "",
            body_text
        ))
        server = smtplib.SMTP(host)
        server.sendmail(from_addr, [to_addr], BODY)
        server.quit()
    else:
        print("Configure the mail server!")
