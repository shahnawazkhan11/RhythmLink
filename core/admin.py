"""
Custom Admin Site Configuration
"""
from django.contrib import admin
from django.contrib.admin import AdminSite


class RhythmLinkAdminSite(AdminSite):
    """Custom Admin Site for RhythmLink"""
    
    site_header = "RhythmLink Administration"
    site_title = "RhythmLink Admin Portal"
    index_title = "Welcome to RhythmLink Event Management System"
    
    def each_context(self, request):
        """
        Add custom context data to all admin pages
        """
        context = super().each_context(request)
        
        # Add custom dashboard data
        if request.user.is_authenticated:
            from events.models import Event
            from customers.models import Booking
            from analytics.models import EventAnalytics
            
            try:
                context['total_events'] = Event.objects.count()
                context['total_bookings'] = Booking.objects.count()
                context['upcoming_events'] = Event.objects.filter(status='upcoming').count()
                
                # Get analytics summary
                from django.db.models import Sum
                total_revenue = EventAnalytics.objects.aggregate(
                    total=Sum('total_revenue')
                )['total'] or 0
                context['total_revenue'] = total_revenue
            except:
                pass
        
        return context


# Create custom admin site instance
# admin_site = RhythmLinkAdminSite(name='rhythmlink_admin')
