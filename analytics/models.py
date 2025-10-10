from django.db import models
from django.contrib.auth.models import User


class EventAnalytics(models.Model):
    """Analytics data for events - can be materialized view or cached data"""
    event = models.OneToOneField('events.Event', on_delete=models.CASCADE, related_name='analytics')
    total_bookings = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    booking_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tickets_available = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.event.name}"
    
    class Meta:
        indexes = [
            models.Index(fields=['last_updated']),
            models.Index(fields=['total_revenue']),
            models.Index(fields=['booking_percentage']),
        ]


class ManagerDashboardConfig(models.Model):
    """Configuration for manager dashboard metrics"""
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_configs')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='dashboard_configs')
    metric_name = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['manager', 'event', 'metric_name']
        ordering = ['display_order']


class DashboardSnapshot(models.Model):
    """Daily snapshots of key metrics for historical analysis"""
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='snapshots')
    date = models.DateField(auto_now_add=True)
    bookings_count = models.IntegerField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    booking_velocity = models.DecimalField(max_digits=8, decimal_places=2)  # bookings per day
    current_price_tier = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.event.name} - {self.date}"
    
    class Meta:
        unique_together = ['event', 'date']
        ordering = ['-date']