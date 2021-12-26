from django.core.mail import EmailMessage
# from django.core.mail import send_mail


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'], body=data['message'], from_email=data['email_from'], to=[data['email_to']])
        email.send()
