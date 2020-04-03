import os
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage
from typing import List

from src.subscriber import Subscriber


class Sender:
    def __init__(self, path_to_email_content: str):
        self.path_to_email_content = path_to_email_content

    def send_to(self, subscribers: List[Subscriber]):
        smtp_obj = smtplib.SMTP("smtp.mail.me.com", 587)
        smtp_obj.starttls()
        smtp_obj.login(
            os.environ["FTF_EMAIL_ADDRESS"], os.environ["FTF_EMAIL_PASSWORD"]
        )

        me = smtp_obj.user

        for subscriber in subscribers:
            you = Address(subscriber.name, addr_spec=subscriber.email)

            msg = EmailMessage()
            msg["Subject"] = "Four Track Friday"
            msg["From"] = me
            msg["To"] = you

            with open(self.path_to_email_content, "r") as html_file:
                body = html_file.read()

            msg.set_content(body, subtype="html")

            print(f"Sending email to {subscriber.name} at {subscriber.email}...")
            try:
                smtp_obj.send_message(msg=msg)
            except Exception as e:
                print(
                    f"There was a problem sending email to {subscriber.name} at {subscriber.email}: {e}"
                )

        print(f"Finished sending emails to {len(subscribers)} people.")

        smtp_obj.quit()
