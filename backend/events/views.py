from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Event, Venue, EventType
from .serializers import EventSerializer, VenueSerializer, EventTypeSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().select_related('venue', 'event_type').order_by('-date', '-created_at')
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'venue', 'event_type', 'date']
    search_fields = ['name', 'description', 'venue__name', 'venue__city', 'event_type__name']
    ordering_fields = ['date', 'created_at', 'name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Handle custom search parameter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(venue__name__icontains=search) |
                Q(venue__city__icontains=search) |
                Q(event_type__name__icontains=search)
            )
        
        return queryset


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all().order_by('name')
    serializer_class = VenueSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city', 'location']


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all().order_by('name')
    serializer_class = EventTypeSerializer
