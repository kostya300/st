from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.core.mail import send_mail
from django.urls import reverse
import uuid
from django.conf import settings
from pyexpat.errors import messages
from django.utils.timezone import now


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
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    def __str__(self):
        return self.user.email


    def send_verification_email(self):
        link = reverse('users:email_verification',kwargs={'email':self.user.email,'code':self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение для {self.user.username}'
        message = 'Для подтверждения учётной записи {} перейдите по ссылке: {}'.format(self.user.email,verification_link)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )
    def is_expired(self):
        return True if now() >= self.expiration else False
# confirm email adress end