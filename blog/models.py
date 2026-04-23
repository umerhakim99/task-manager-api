from django.db import models
from django.conf import settings


class Contact(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100)
    email       = models.EmailField(unique=True)
    phone       = models.CharField(max_length=20, blank=True)
    message     = models.TextField()
    address     = models.CharField(max_length=255, blank=True)
    gender      = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    birthday    = models.DateField(null=True, blank=True)
    company     = models.CharField(max_length=100, blank=True)
    website     = models.URLField(blank=True)
    is_favorite = models.BooleanField(default=False)
    status      = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name