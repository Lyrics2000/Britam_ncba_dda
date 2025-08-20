from django.db import models

# Create your models here.

class AuthToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = "Auth Token"
        verbose_name_plural = "Auth Tokens"
        ordering = ['-created_at']
