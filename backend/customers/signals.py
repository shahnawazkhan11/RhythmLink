from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking
from pricing.services import DynamicPricingService


@receiver(post_save, sender=Booking)
def update_pricing_on_booking(sender, instance, created, **kwargs):
    """Update ticket prices when a new booking is created"""
    if created and instance.status == 'confirmed':
        # Mark tickets as booked
        for ticket in instance.tickets.all():
            ticket.status = 'booked'
            ticket.save()
        
        # Update pricing for the event
        DynamicPricingService.update_ticket_prices(instance.event)


@receiver(post_delete, sender=Booking)
def update_pricing_on_cancellation(sender, instance, **kwargs):
    """Update ticket prices when a booking is cancelled"""
    # Mark tickets as available again
    for ticket in instance.tickets.all():
        ticket.status = 'available'
        ticket.save()
    
    # Update pricing for the event
    DynamicPricingService.update_ticket_prices(instance.event)