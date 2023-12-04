from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')  # Add a default value
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    phone_number = models.CharField(max_length=15, default='')

    # Additional fields related to the profile
    # Add more fields as required for your profile

    def __str__(self):
        return self.user.username
