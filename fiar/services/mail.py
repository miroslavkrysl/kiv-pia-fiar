import smtplib
from email.message import EmailMessage

from fiar.utils import async_task


class MailService:
    def __init__(self,
                 host: str,
                 port: int,
                 user: str,
                 password: str,
                 ssl: bool,
                 tls: bool,
                 from_name: str,
                 from_addr: str,):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ssl = ssl
        self.tls = tls
        self.from_name = from_name
        self.from_addr = from_addr

    def send(self, subject: str, receiver: str, content: str):
        msg = EmailMessage()
        msg.set_content(content, subtype='html')

        msg['Subject'] = subject
        msg['From'] = self._make_sender()
        msg['To'] = receiver

        self._send_async(msg)

    def _make_sender(self):
        sender = '<' + self.from_addr + '>'

        if self.from_name is not None:
            sender = self.from_name + ' ' + sender

        return sender

    @async_task
    def _send_async(self, msg):

        if self.ssl:
            server = smtplib.SMTP_SSL(self.host, self.port)
        else:
            server = smtplib.SMTP(self.host, self.port)

        if self.tls:
            server.starttls()

        server.login(self.user, self.password)
        server.send_message(msg)
        server.close()
