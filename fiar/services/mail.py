import smtplib
from email.message import EmailMessage

from fiar.utils import async_task


class MailService:
    def __init__(self,
                 host: str,
                 port: int,
                 username: str,
                 password: str,
                 ssl: bool,
                 tls: bool,
                 sender_name: str,
                 sender_addr: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl = ssl
        self.tls = tls
        self.sender_name = sender_name
        self.sender_addr = sender_addr

    def send(self, subject: str, recipient: str, content: str):
        """
        Send an email.
        :param subject: Email subject.
        :param recipient: Recipient email address.
        :param content: Email content
        """
        msg = EmailMessage()
        msg.set_content(content, subtype='html')

        msg['Subject'] = subject
        msg['From'] = self._make_sender()
        msg['To'] = recipient

        self._send_async(msg)

    def _make_sender(self):
        sender = '<' + self.sender_addr + '>'

        if self.sender_name is not None:
            sender = self.sender_name + ' ' + sender

        return sender

    @async_task
    def _send_async(self, msg):

        if self.ssl:
            server = smtplib.SMTP_SSL(self.host, self.port)
        else:
            server = smtplib.SMTP(self.host, self.port)

        if self.tls:
            server.starttls()

        server.login(self.username, self.password)
        server.send_message(msg)
        server.close()
