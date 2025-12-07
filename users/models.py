# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('tester', 'Security Tester'),
        ('admin', 'System Administrator'),
        ('client', 'Client/Manager'),
        ('manager', 'UserManager'), 
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='tester',
        verbose_name='System Role'
    )

    
    def __str__(self):
        return self.username