import os
import smtplib
import sys
from configparser import ConfigParser


def send_email(body_text):
    """
    Send an email
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "conf.ini")
    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Config not found! Exiting!")
        sys.exit(1)
    host = cfg.get("smtp", "server")
    from_addr = cfg.get("smtp", "from_addr")
    to_addr = cfg.get("smtp", "to_addr")
    subject = cfg.get("smtp", "subject")
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
