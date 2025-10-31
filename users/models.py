from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
# Create your models here.

class User(AbstractUser):
    image = models.ImageField(
        upload_to='images/users_images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )

    def __str__(self):
        return self.username