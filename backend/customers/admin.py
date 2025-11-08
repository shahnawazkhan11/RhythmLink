from django.contrib import admin
from .models import Customer, Ticket, Booking, Feedback, FanInteraction


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'country', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['country', 'created_at']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['event', 'seat_number', 'section', 'base_price', 'final_price', 'status', 'created_at']
    list_filter = ['status', 'event__date', 'created_at']
    search_fields = ['event__name', 'seat_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'event', 'total_amount', 'status', 'booking_date']
    list_filter = ['status', 'booking_date', 'event__date']
    search_fields = ['customer__user__username', 'event__name', 'payment_reference']
    readonly_fields = ['booking_date']
    filter_horizontal = ['tickets']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['customer', 'event', 'rating', 'would_recommend', 'created_at']
    list_filter = ['rating', 'would_recommend', 'created_at']
    search_fields = ['customer__user__username', 'event__name', 'comment']
    readonly_fields = ['created_at']


@admin.register(FanInteraction)
class FanInteractionAdmin(admin.ModelAdmin):
    list_display = ['fan', 'track', 'interaction_type', 'timestamp', 'device_type']
    list_filter = ['interaction_type', 'device_type', 'timestamp']
    search_fields = ['fan__user__username', 'track__track_name', 'track__album__album_name']
    readonly_fields = ['created_at']
    date_hierarchy = 'timestamp'