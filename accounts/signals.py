from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=UserProfile)
def assign_user_groups(sender, instance, **kwargs):
    """Assign users to appropriate groups based on role"""
    # Create groups if they don't exist
    manager_group, _ = Group.objects.get_or_create(name='Event Managers')
    customer_group, _ = Group.objects.get_or_create(name='Customers')
    admin_group, _ = Group.objects.get_or_create(name='Administrators')
    
    # Clear existing groups
    instance.user.groups.clear()
    
    # Assign to appropriate group
    if instance.role == 'manager':
        instance.user.groups.add(manager_group)
    elif instance.role == 'customer':
        instance.user.groups.add(customer_group)
    elif instance.role == 'admin':
        instance.user.groups.add(admin_group)
        instance.user.is_staff = True
        instance.user.save()