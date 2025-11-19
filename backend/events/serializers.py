from rest_framework import serializers
from .models import Event, Venue, EventType, Performs, EventManager
from pricing.services import DynamicPricingService


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ['id', 'name', 'description']


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            'id', 'name', 'location', 'address', 'city', 'state',
            'capacity', 'amenities', 'contact_email', 'contact_phone',
            'latitude', 'longitude', 'is_active', 'created_at'
        ]


class EventSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    event_type_name = serializers.CharField(source='event_type.name', read_only=True)
    available_tickets = serializers.IntegerField(source='available_tickets_count', read_only=True)
    booking_percentage = serializers.FloatField(read_only=True)
    current_price = serializers.SerializerMethodField()
    current_tier_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'date', 'start_time', 'end_time',
            'venue', 'venue_name', 'event_type', 'event_type_name',
            'poster_image', 'ticket_price', 'current_price', 'current_tier_name',
            'available_tickets', 'booking_percentage', 'max_tickets_per_customer',
            'is_active', 'created_at', 'updated_at'
        ]
    
    def get_current_price(self, obj):
        """Get the current dynamic price for this event"""
        current_tier = DynamicPricingService.calculate_current_tier(obj)
        return str(current_tier.price) if current_tier else str(obj.ticket_price)
    
    def get_current_tier_name(self, obj):
        """Get the current tier name"""
        current_tier = DynamicPricingService.calculate_current_tier(obj)
        return current_tier.tier_name if current_tier else None