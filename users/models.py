from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')


    # Dunder str method to display how we want it to be displayed, or else it will display as profileObject
    def __str__(self):
        return f'{self.user.username} Profile'
