from django.core.mail import EmailMessage
# from django.core.mail import send_mail


import threading

class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'], body=data['message'], from_email=data['email_from'], to=[data['email_to']])
        # email.send()
        EmailThread(email).start()
        
        
        