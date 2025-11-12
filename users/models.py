from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.core.mail import send_mail
import uuid

# Create your models here.

class User(AbstractUser):
    image = models.ImageField(
        upload_to='images/users_images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    is_verified_email = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile', args=(self.id,))


# confirm email adress



class EmailVerification(models.Model):
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    def __str__(self):
        return self.user.email


    def send_verification_email(self):
        send_mail(
            subject='Тема письма',
            message='Текст письма',
            from_email='sender@example.com',
            recipient_list=[self.user.email],
            fail_silently=False,
        )