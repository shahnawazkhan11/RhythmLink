from django.contrib import admin
from .models import EventAnalytics, ManagerDashboardConfig, DashboardSnapshot


@admin.register(EventAnalytics)
class EventAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['event', 'total_bookings', 'total_revenue', 'avg_rating', 'booking_percentage', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['event__name']
    readonly_fields = ['last_updated']


@admin.register(ManagerDashboardConfig)
class ManagerDashboardConfigAdmin(admin.ModelAdmin):
    list_display = ['manager', 'event', 'metric_name', 'display_order', 'is_visible']
    list_filter = ['is_visible', 'metric_name']
    search_fields = ['manager__username', 'event__name']


@admin.register(DashboardSnapshot)
class DashboardSnapshotAdmin(admin.ModelAdmin):
    list_display = ['event', 'date', 'bookings_count', 'revenue', 'booking_velocity']
    list_filter = ['date']
    search_fields = ['event__name']
    readonly_fields = ['date']