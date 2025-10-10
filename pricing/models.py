from django.db import models
from django.contrib.auth.models import User


class PriceTier(models.Model):
    """Dynamic pricing tiers for events"""
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='price_tiers')
    tier_name = models.CharField(max_length=50)  # e.g., "Early Bird", "Regular", "Premium"
    tier_percentage_start = models.IntegerField()  # 0-100 (percentage of capacity sold)
    tier_percentage_end = models.IntegerField()    # 0-100 (percentage of capacity sold)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_price_tiers')
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.event.name} - {self.tier_name} ({self.tier_percentage_start}-{self.tier_percentage_end}%)"
    
    def save(self, *args, **kwargs):
        # Validate tier ranges don't overlap
        overlapping_tiers = PriceTier.objects.filter(
            event=self.event,
            is_active=True
        ).exclude(id=self.id)
        
        for tier in overlapping_tiers:
            if not (self.tier_percentage_end <= tier.tier_percentage_start or 
                   self.tier_percentage_start >= tier.tier_percentage_end):
                raise ValueError(f"Price tier overlaps with existing tier: {tier.tier_name}")
        
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ['event', 'tier_percentage_start', 'tier_percentage_end']
        ordering = ['event', 'tier_percentage_start']
        indexes = [
            models.Index(fields=['event', 'is_active']),
        ]


class PriceHistory(models.Model):
    """Track price changes over time"""
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='price_history')
    old_tier = models.ForeignKey(PriceTier, on_delete=models.SET_NULL, null=True, blank=True, related_name='old_price_history')
    new_tier = models.ForeignKey(PriceTier, on_delete=models.CASCADE, related_name='new_price_history')
    booking_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    changed_at = models.DateTimeField(auto_now_add=True)
    tickets_sold_count = models.IntegerField()
    
    def __str__(self):
        return f"{self.event.name} - {self.booking_percentage}% - {self.new_tier.price}"
    
    class Meta:
        ordering = ['-changed_at']
        indexes = [
            models.Index(fields=['event', 'changed_at']),
        ]