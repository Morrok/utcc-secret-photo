from django.db import models


class CookieConsent(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    consent_given = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.consent_given}'