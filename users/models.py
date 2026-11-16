from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('commuter', 'Commuter'),
        ('conductor', 'Conductor'),
        ('driver', 'Driver'),
    ]
    # Supabase UUID for connecting with Supabase Auth (if used)
    supabase_uid = models.UUIDField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='commuter')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
