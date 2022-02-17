import os
import smtplib
import sys
from configparser import ConfigParser


def send_email(body_text):
    """
    Send an email
    """
    #base_path = os.path.dirname(os.path.abspath(__file__))
    host = os.environ.get("SERVER")
    from_addr = os.environ.get("FROM_ADDR")
    to_addr = os.environ.get("TO_ADDR")
    subject = os.environ.get("SUBJECT")
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


if __name__ == '__main__':
    send_email("Test Letter")
    print("Mail has been sent")
