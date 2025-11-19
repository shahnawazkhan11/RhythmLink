"""
Test to verify revenue calculation from bookings
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from customers.models import Booking
from events.models import Event, EventManager
from django.contrib.auth.models import User
from django.db.models import Sum

print("\n" + "="*60)
print("REVENUE VERIFICATION TEST")
print("="*60)

# Get all bookings
all_bookings = Booking.objects.all()
print(f"\n📊 Total Bookings in System: {all_bookings.count()}")

if all_bookings.exists():
    print("\n💰 Booking Details:")
    for booking in all_bookings:
        print(f"  - Booking #{booking.id}")
        print(f"    Event: {booking.event.name}")
        print(f"    Customer: {booking.customer.user.username}")
        print(f"    Amount: ${booking.total_amount}")
        print(f"    Status: {booking.status}")
        print(f"    Date: {booking.booking_date}")
        print(f"    Tickets: {booking.tickets.count()}")
        print()
    
    # Calculate total revenue
    confirmed_bookings = Booking.objects.filter(status='confirmed')
    total_revenue = confirmed_bookings.aggregate(total=Sum('total_amount'))['total'] or 0
    
    print(f"\n📈 Revenue Summary:")
    print(f"  Total Bookings: {all_bookings.count()}")
    print(f"  Confirmed Bookings: {confirmed_bookings.count()}")
    print(f"  Total Revenue: ${total_revenue}")
else:
    print("\n⚠️  NO BOOKINGS FOUND!")
    print("\nTo create a booking:")
    print("1. Go to http://localhost:3000/events")
    print("2. Click on an event")
    print("3. Select tickets and book")

# Check manager setup
print("\n" + "="*60)
print("MANAGER VERIFICATION")
print("="*60)

managers = EventManager.objects.all()
print(f"\n👔 Total Managers: {managers.count()}")

if managers.exists():
    for manager in managers:
        print(f"\n  Manager: {manager.user.username} ({manager.user.get_full_name()})")
        managed_events = manager.managed_events.all()
        print(f"  Manages {managed_events.count()} events:")
        
        manager_revenue = 0
        for event in managed_events:
            event_bookings = Booking.objects.filter(event=event, status='confirmed')
            event_revenue = event_bookings.aggregate(total=Sum('total_amount'))['total'] or 0
            manager_revenue += float(event_revenue)
            print(f"    - {event.name}: ${event_revenue} ({event_bookings.count()} bookings)")
        
        print(f"  Total Revenue: ${manager_revenue}")
else:
    print("\n⚠️  NO MANAGERS FOUND!")
    print("\nTo check which user is a manager:")
    staff_users = User.objects.filter(is_staff=True)
    print(f"\nStaff users: {staff_users.count()}")
    for user in staff_users:
        print(f"  - {user.username} (is_staff={user.is_staff})")

print("\n" + "="*60)
