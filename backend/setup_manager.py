"""
Setup manager and link events
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event, EventManager

print("\n" + "="*60)
print("MANAGER SETUP")
print("="*60)

# Find the manager user
manager_username = input("\nEnter manager username (e.g., manish1): ").strip()

try:
    manager_user = User.objects.get(username=manager_username)
    print(f"\n✓ Found user: {manager_user.username}")
    print(f"  Email: {manager_user.email}")
    print(f"  Staff: {manager_user.is_staff}")
except User.DoesNotExist:
    print(f"\n✗ User '{manager_username}' not found!")
    print("\nAvailable users:")
    for user in User.objects.all():
        print(f"  - {user.username}")
    exit(1)

# Make sure user is staff
if not manager_user.is_staff:
    print(f"\n⚠️  Making {manager_user.username} a staff member...")
    manager_user.is_staff = True
    manager_user.save()
    print("  ✓ Done!")

# Create or get EventManager profile
manager_profile, created = EventManager.objects.get_or_create(
    user=manager_user,
    defaults={
        'can_manage_pricing': True,
        'is_active': True
    }
)

if created:
    print(f"\n✓ Created EventManager profile for {manager_user.username}")
else:
    print(f"\n✓ EventManager profile already exists for {manager_user.username}")

# Link all events to this manager
events = Event.objects.all()
print(f"\nFound {events.count()} events. Linking to manager...")

for event in events:
    manager_profile.managed_events.add(event)
    print(f"  ✓ Linked: {event.name}")

manager_profile.save()

print("\n" + "="*60)
print("SETUP COMPLETE!")
print("="*60)
print(f"\nManager: {manager_user.username}")
print(f"Manages: {manager_profile.managed_events.count()} events")
print(f"\nNow refresh the manager dashboard: http://localhost:3000/manager")
print("="*60 + "\n")
