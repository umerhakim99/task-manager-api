from django.db import models
from django.contrib.auth.models import AbstractUser


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail




class CustomUser(AbstractUser):
    phone           = models.CharField(max_length=20, blank=True)
    bio             = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    email = models.EmailField(unique=True)



    def __str__(self):
        return self.username






# Signal
@receiver(post_save, sender=CustomUser)
def welcome_user(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Welcome to Task Manager!',
            message=f'Hi {instance.username}, your account has been created successfully.',
            from_email='your_email@gmail.com',
            recipient_list=[instance.email],
        )
        print(f"Welcome email sent to {instance.email}")