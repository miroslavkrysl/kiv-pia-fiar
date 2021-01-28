from flask_mail import Mail

from fiar.persistence.models import User


class MailService:

    def __init__(self, mail: Mail):
        self.mail = mail

    def send_password_reset_email(self, user: User):
        # TODO
        pass