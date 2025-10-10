from django.contrib import admin
from .models import PriceTier, PriceHistory


@admin.register(PriceTier)
class PriceTierAdmin(admin.ModelAdmin):
    list_display = ['event', 'tier_name', 'tier_percentage_start', 'tier_percentage_end', 
                    'price', 'created_by_manager', 'is_active', 'created_date']
    list_filter = ['is_active', 'created_date', 'event__date']
    search_fields = ['event__name', 'tier_name', 'created_by_manager__username']
    list_editable = ['is_active']
    ordering = ['event', 'tier_percentage_start']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Event Managers').exists():
            # Managers can only see price tiers for their events
            return qs.filter(created_by_manager=request.user)
        return qs


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['event', 'booking_percentage', 'new_tier', 'tickets_sold_count', 'changed_at']
    list_filter = ['changed_at', 'event__date']
    search_fields = ['event__name']
    ordering = ['-changed_at']
    readonly_fields = ['changed_at']
    
    def has_add_permission(self, request):
        # Price history is auto-generated, not manually added
        return False
    
    def has_change_permission(self, request, obj=None):
        # Price history should not be editable
        return False