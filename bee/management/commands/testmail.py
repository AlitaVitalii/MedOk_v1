from django.core.mail import send_mail
from django.core.management import BaseCommand


class Command(BaseCommand):
    send_mail(
        "ActionCreate2",
        "Here is the message.",
        "alita.v@ukr.net",
        ["alita.avs@gmail.com"],
        fail_silently=False,
    )
