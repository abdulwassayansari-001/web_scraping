from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

USER = get_user_model()


class LinkCounter(models.Model):
    requester = models.OneToOneField(USER, on_delete=models.CASCADE)
    sent_count = models.IntegerField()

    def __str__(self):
        return str(self.requester.get_username())

    def __repr__(self):
        return str(self.requester.get_username())

class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - Verified on {self.verification_date}'
