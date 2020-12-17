from django.core.mail import EmailMessage
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['mail_subject'], body=data['mail_message'], to=data['recipient_email'])
        EmailThread(email).start()
