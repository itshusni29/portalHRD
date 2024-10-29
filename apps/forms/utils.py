

from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import BadHeaderError

def send_notification_email(subject, message, recipient_list):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,            
            fail_silently=False,
        )
    except BadHeaderError:
        print("Invalid header found.")
    except Exception as e:
        print(f"An error occurred: {e}")
