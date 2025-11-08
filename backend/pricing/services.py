from django.db.models import Count, Q
from decimal import Decimal
from .models import PriceTier, PriceHistory
from customers.models import Ticket
from events.models import Event


class DynamicPricingService:
    """Service class for handling dynamic pricing logic"""
    
    @staticmethod
    def calculate_current_tier(event):
        """
        Calculate the current price tier based on booking percentage
        """
        booking_percentage = event.booking_percentage
        
        # Get active price tiers for this event
        current_tier = PriceTier.objects.filter(
            event=event,
            is_active=True,
            tier_percentage_start__lte=booking_percentage,
            tier_percentage_end__gt=booking_percentage
        ).first()
        
        return current_tier
    
    @staticmethod
    def update_ticket_prices(event):
        """
        Update all available tickets for an event based on current tier
        """
        current_tier = DynamicPricingService.calculate_current_tier(event)
        
        if current_tier:
            # Update all available tickets to current tier price
            updated_count = Ticket.objects.filter(
                event=event,
                status='available'
            ).update(
                final_price=current_tier.price,
                current_tier=current_tier
            )
            
            # Log price change
            PriceHistory.objects.create(
                event=event,
                new_tier=current_tier,
                booking_percentage=Decimal(str(event.booking_percentage)),
                tickets_sold_count=Ticket.objects.filter(
                    event=event, 
                    status='booked'
                ).count()
            )
            
            return updated_count, current_tier.price
        
        return 0, None
    
    @staticmethod
    def create_default_price_tiers(event, manager, base_price):
        """
        Create default price tiers for an event
        """
        default_tiers = [
            {
                'tier_name': 'Early Bird',
                'start': 0,
                'end': 30,
                'multiplier': 0.8
            },
            {
                'tier_name': 'Regular',
                'start': 30,
                'end': 70,
                'multiplier': 1.0
            },
            {
                'tier_name': 'Premium',
                'start': 70,
                'end': 100,
                'multiplier': 1.5
            }
        ]
        
        created_tiers = []
        for tier_data in default_tiers:
            tier = PriceTier.objects.create(
                event=event,
                tier_name=tier_data['tier_name'],
                tier_percentage_start=tier_data['start'],
                tier_percentage_end=tier_data['end'],
                price=base_price * Decimal(str(tier_data['multiplier'])),
                created_by_manager=manager
            )
            created_tiers.append(tier)
        
        return created_tiers