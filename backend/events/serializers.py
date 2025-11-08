from rest_framework import serializers
from .models import Event, Venue, EventType, Performs, EventManager


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
    
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'date', 'start_time', 'end_time',
            'venue', 'venue_name', 'event_type', 'event_type_name',
            'poster_image', 'ticket_price', 'max_tickets_per_customer',
            'is_active', 'created_at', 'updated_at'
        ]