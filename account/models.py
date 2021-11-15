from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    avatar = models.ImageField(upload_to='users_avatars/', blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'moviegoer.jpg'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

