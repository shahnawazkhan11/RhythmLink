from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    """Extended user profile with role management"""
    USER_ROLES = [
        ('manager', 'Event Manager'),
        ('customer', 'Customer/Audience'),
        ('admin', 'System Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=USER_ROLES, default='customer')
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"
    
    def is_manager(self):
        return self.role == 'manager'
    
    def is_customer(self):
        return self.role == 'customer'
    
    def is_admin(self):
        return self.role == 'admin'
    
    class Meta:
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['user', 'role']),
        ]