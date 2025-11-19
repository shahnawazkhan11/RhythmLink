"""
Test script to demonstrate Dynamic Pricing System

This script tests the automatic price adjustment based on booking volume.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from events.models import Event
from customers.models import Ticket, Booking, Customer
from pricing.models import PriceTier, PriceHistory
from pricing.services import DynamicPricingService
from django.contrib.auth.models import User


def test_dynamic_pricing():
    print("\n" + "="*60)
    print("DYNAMIC PRICING SYSTEM TEST")
    print("="*60)
    
    # Get or create test user
    user, _ = User.objects.get_or_create(
        username='test_customer',
        defaults={'email': 'test@example.com'}
    )
    customer, _ = Customer.objects.get_or_create(user=user)
    
    # Get a sample event
    event = Event.objects.filter(is_active=True).first()
    
    if not event:
        print("\n❌ No active events found. Please create an event first.")
        return
    
    print(f"\n📅 Event: {event.name}")
    print(f"   Base Price: ${event.ticket_price}")
    
    # Check if price tiers exist
    price_tiers = PriceTier.objects.filter(event=event, is_active=True).order_by('tier_percentage_start')
    
    if not price_tiers.exists():
        print("\n⚠️  No price tiers found. Creating default tiers...")
        manager = User.objects.filter(is_staff=True).first() or user
        DynamicPricingService.create_default_price_tiers(event, manager, event.ticket_price)
        price_tiers = PriceTier.objects.filter(event=event, is_active=True).order_by('tier_percentage_start')
    
    print("\n💰 Price Tiers:")
    for tier in price_tiers:
        print(f"   {tier.tier_name:15} {tier.tier_percentage_start:3}%-{tier.tier_percentage_end:3}%  →  ${tier.price}")
    
    # Current booking status
    total_tickets = event.tickets.count()
    booked_tickets = event.tickets.filter(status='booked').count()
    available_tickets = event.available_tickets_count
    booking_pct = event.booking_percentage
    
    print(f"\n📊 Current Status:")
    print(f"   Total Tickets: {total_tickets}")
    print(f"   Booked: {booked_tickets}")
    print(f"   Available: {available_tickets}")
    print(f"   Booking: {booking_pct:.2f}%")
    
    # Current tier
    current_tier = DynamicPricingService.calculate_current_tier(event)
    if current_tier:
        print(f"\n🎯 Current Tier: {current_tier.tier_name}")
        print(f"   Current Price: ${current_tier.price}")
    else:
        print("\n⚠️  No current tier (may need to create tickets)")
    
    # Check price history
    recent_history = PriceHistory.objects.filter(event=event).order_by('-changed_at')[:5]
    if recent_history.exists():
        print(f"\n📈 Recent Price Changes:")
        for history in recent_history:
            print(f"   {history.changed_at.strftime('%Y-%m-%d %H:%M')} | "
                  f"{history.booking_percentage:.1f}% booked | "
                  f"${history.new_tier.price} ({history.new_tier.tier_name})")
    else:
        print("\n📈 No price change history yet")
    
    print("\n" + "="*60)
    print("HOW IT WORKS:")
    print("="*60)
    print("1. When an event is created, default price tiers are auto-generated:")
    print("   - Early Bird (0-30%): 80% of base price")
    print("   - Regular (30-70%): 100% of base price")
    print("   - Premium (70-100%): 150% of base price")
    print("\n2. When a booking is created (via BookingCreateView):")
    print("   - Signal handler in customers/signals.py is triggered")
    print("   - DynamicPricingService.update_ticket_prices() is called")
    print("   - All available tickets are updated to current tier price")
    print("   - Price change is logged in PriceHistory")
    print("\n3. All API responses include:")
    print("   - current_price: The active dynamic price")
    print("   - current_tier_name: e.g., 'Early Bird', 'Regular', 'Premium'")
    print("   - booking_percentage: Current booking %")
    print("="*60 + "\n")


if __name__ == '__main__':
    test_dynamic_pricing()
