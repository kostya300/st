import uuid
from celery import shared_task
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta
from .models import User,EmailVerification

@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = timezone.now() + timedelta(hours=48)
    record = EmailVerification.objects.create(
        user=user,
        expiration=expiration
    )
    record.send_verification_email()