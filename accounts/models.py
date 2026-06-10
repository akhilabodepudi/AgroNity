from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('customer', 'Customer'),
        ('admin', 'Administrator'),
    )
    phone_number = models.CharField(max_length=15, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_approved = models.BooleanField(default=True)  # customers auto-approved

    def requires_approval(self) -> bool:
        return self.role in ('farmer', 'admin')