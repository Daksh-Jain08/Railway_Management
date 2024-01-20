from celery import shared_task
from .models import *
from trains.models import *
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_ticket_mail():
    subject = "Subject"
    message = "This is a test message!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["jain.daksh0808@gmail.com"]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)
    return "Done"