from django.db import models
from tickets.models import Ticket
from users.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    wallet = models.IntegerField(default=0)
    tickets = models.ForeignKey(Ticket, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
