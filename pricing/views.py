from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from events.models import Event
from .models import PriceTier
from .services import DynamicPricingService


class EventPriceTiersView(generics.RetrieveAPIView):
    """Get all price tiers for an event"""
    
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        tiers = PriceTier.objects.filter(event=event, is_active=True).order_by('tier_percentage_start')
        
        tier_data = [{
            'id': tier.id,
            'tier_name': tier.tier_name,
            'tier_percentage_start': tier.tier_percentage_start,
            'tier_percentage_end': tier.tier_percentage_end,
            'price': str(tier.price),
            'created_date': tier.created_date,
            'is_active': tier.is_active
        } for tier in tiers]
        
        return Response({
            'event_id': event_id,
            'event_name': event.name,
            'tiers': tier_data
        })


class CurrentPriceView(generics.RetrieveAPIView):
    """Get current price for an event based on booking percentage"""
    
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        current_tier = DynamicPricingService.calculate_current_tier(event)
        
        if not current_tier:
            return Response({
                'error': 'No price tiers configured for this event'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'event_id': event_id,
            'event_name': event.name,
            'current_booking_percentage': float(event.booking_percentage),
            'current_tier': {
                'id': current_tier.id,
                'tier_name': current_tier.tier_name,
                'price': str(current_tier.price),
                'tier_range': f'{current_tier.tier_percentage_start}-{current_tier.tier_percentage_end}%'
            },
            'available_tickets': event.available_tickets_count,
            'total_tickets': event.tickets.count()
        })