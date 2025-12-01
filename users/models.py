from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.utils.timezone import now
import logging
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone as tz
from django.db import models
from django.core.exceptions import ValidationError
import uuid


logger = logging.getLogger(__name__)

# Create your models here.

class User(AbstractUser):
    image = models.ImageField(
        upload_to='images/users_images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    is_verified_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile', args=(self.id,))







# confirm email adress
class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )
    expiration = models.DateTimeField(verbose_name="Срок действия")

    class Meta:
        indexes = [
            models.Index(fields=['expiration']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    def clean(self):
        if self.expiration < tz.now():
            raise ValidationError("Срок действия не может быть в прошлом")

    def is_expired(self):
        return tz.now() > self.expiration

    @property
    def verification_url(self):
        link = reverse('users:email_verification', kwargs={
            'email': self.user.email,
            'code': self.code
        })
        return f'{settings.DOMAIN_NAME}{link}'

    def send_verification_email(self):
        try:
            subject = f'Подтверждение для {self.user.username}'
            message = (
                f'Для подтверждения учётной записи {self.user.email} '
                f'перейдите по ссылке: {self.verification_url}'
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Ошибка отправки письма подтверждения: {e}")
            raise

# confirm email adress end