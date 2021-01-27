from flask_mail import Mail


class MailService:

    def __init__(self, mail: Mail):
        self.mail = mail
