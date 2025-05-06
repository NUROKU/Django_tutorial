import uuid
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin
from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    
class UserActivateTokensManager(models.Manager):

    def activate_user_by_token(self, activate_token):
        user_activate_token = self.filter(
            activate_token=activate_token,
            expired_at__gte=datetime.now() # __gte = greater than equal
        ).first()
        if hasattr(user_activate_token, 'user'):
            user = user_activate_token.user
            user.is_active = True
            user.save()
            return user

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def publish_activate_token(sender, instance, **kwargs):
        if not instance.is_active:
            user_activate_token = UserActivateTokens.objects.create(
                user=instance,
                expired_at=datetime.now()+timedelta(days=settings.ACTIVATION_EXPIRED_DAYS),
            )
            subject = 'Please Activate Your Account'
            message = f'URLにアクセスしてユーザーアクティベーション。\n http://127.0.0.1:8000/users/{user_activate_token.activate_token}/activation/'
        if instance.is_active:
            subject = 'Activated! Your Account!'
            message = 'ユーザーが使用できるようになりました'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [
            instance.email,
        ]
        send_mail(subject, message, from_email, recipient_list)
        
class UserActivateTokens(models.Model):

    token_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activate_token = models.UUIDField(default=uuid.uuid4)
    expired_at = models.DateTimeField()

    objects = UserActivateTokensManager()

