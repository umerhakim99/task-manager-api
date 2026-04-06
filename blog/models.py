from django.db import models
from django.conf import settings




class Contact(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100)
    email       = models.EmailField(unique=True)
    message     = models.TextField()
    status      = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return self.name



