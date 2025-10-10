from django.contrib import admin
from .models import Event, Venue, EventType, Performs, EventManager


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'capacity', 'is_active', 'created_at']
    list_filter = ['city', 'is_active', 'created_at']
    search_fields = ['name', 'city', 'location']
    list_editable = ['is_active']
    ordering = ['name']


class PerformsInline(admin.TabularInline):
    model = Performs
    extra = 1
    autocomplete_fields = ['artist']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'start_time', 'venue', 'event_type', 'ticket_price', 'is_active']
    list_filter = ['date', 'event_type', 'venue__city', 'is_active']
    search_fields = ['name', 'venue__name']
    list_editable = ['is_active']
    date_hierarchy = 'date'
    ordering = ['-date', '-start_time']
    inlines = [PerformsInline]


@admin.register(Performs)
class PerformsAdmin(admin.ModelAdmin):
    list_display = ['artist', 'event', 'performance_time', 'duration_minutes', 'is_headliner']
    list_filter = ['is_headliner', 'event__date']
    search_fields = ['artist__name', 'event__name']


@admin.register(EventManager)
class EventManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'contact_phone', 'can_manage_pricing', 'is_active', 'created_at']
    list_filter = ['can_manage_pricing', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    list_editable = ['can_manage_pricing', 'is_active']
    filter_horizontal = ['managed_events']
