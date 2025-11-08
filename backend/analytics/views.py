from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Avg, Count, Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from events.models import Event, EventManager
from .models import EventAnalytics


class EventDashboardView(generics.RetrieveAPIView):
    """Get comprehensive dashboard metrics for a specific event"""
    
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        
        # Get or compute analytics
        try:
            analytics = EventAnalytics.objects.get(event=event)
        except EventAnalytics.DoesNotExist:
            # Compute on the fly
            tickets = event.tickets.all()
            bookings = event.bookings.filter(status__in=['confirmed', 'pending'])
            feedback = event.feedback.all()
            
            total_tickets = tickets.count()
            booked_tickets = tickets.filter(status='booked').count()
            total_revenue = bookings.aggregate(total=Sum('total_amount'))['total'] or 0
            avg_rating = feedback.aggregate(avg=Avg('rating'))['avg']
            booking_percentage = (booked_tickets / total_tickets * 100) if total_tickets > 0 else 0
            
            analytics_data = {
                'total_bookings': bookings.count(),
                'total_revenue': float(total_revenue),
                'avg_rating': float(avg_rating) if avg_rating else None,
                'booking_percentage': float(booking_percentage),
                'tickets_available': tickets.filter(status='available').count()
            }
        else:
            analytics_data = {
                'total_bookings': analytics.total_bookings,
                'total_revenue': float(analytics.total_revenue),
                'avg_rating': float(analytics.avg_rating) if analytics.avg_rating else None,
                'booking_percentage': float(analytics.booking_percentage),
                'tickets_available': analytics.tickets_available
            }
        
        # Revenue by tier
        revenue_by_tier = event.bookings.filter(status='confirmed').values(
            'tickets__current_tier__tier_name'
        ).annotate(
            tier_revenue=Sum('total_amount'),
            tier_bookings=Count('id')
        )
        
        # Booking velocity (last 7 days)
        from datetime import datetime, timedelta
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_bookings = event.bookings.filter(
            booking_date__gte=seven_days_ago,
            status='confirmed'
        ).count()
        booking_velocity = recent_bookings / 7.0
        
        # Customer demographics (top genres from customer preferences)
        top_genres = event.bookings.filter(
            status='confirmed'
        ).values(
            'customer__preferred_genres__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        return Response({
            'event': {
                'id': event.id,
                'name': event.name,
                'date': event.date,
                'venue': event.venue.name,
                'total_capacity': event.venue.capacity
            },
            'analytics': analytics_data,
            'revenue_by_tier': list(revenue_by_tier),
            'booking_velocity_per_day': round(booking_velocity, 2),
            'top_customer_genres': list(top_genres),
            'last_updated': analytics.last_updated if hasattr(analytics, 'last_updated') else None
        })


class ManagerDashboardView(generics.ListAPIView):
    """Get dashboard overview for all events managed by the current user"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get events managed by this user
        try:
            manager = EventManager.objects.get(user=user)
            events = manager.managed_events.all()
        except EventManager.DoesNotExist:
            events = Event.objects.none()
        
        # Aggregate data for all events
        event_summaries = []
        total_revenue = 0
        total_bookings = 0
        
        for event in events:
            try:
                analytics = EventAnalytics.objects.get(event=event)
                event_data = {
                    'id': event.id,
                    'name': event.name,
                    'date': event.date,
                    'venue': event.venue.name,
                    'total_bookings': analytics.total_bookings,
                    'total_revenue': float(analytics.total_revenue),
                    'booking_percentage': float(analytics.booking_percentage),
                    'avg_rating': float(analytics.avg_rating) if analytics.avg_rating else None,
                    'tickets_available': analytics.tickets_available
                }
                total_revenue += float(analytics.total_revenue)
                total_bookings += analytics.total_bookings
            except EventAnalytics.DoesNotExist:
                event_data = {
                    'id': event.id,
                    'name': event.name,
                    'date': event.date,
                    'venue': event.venue.name,
                    'total_bookings': 0,
                    'total_revenue': 0,
                    'booking_percentage': 0,
                    'avg_rating': None,
                    'tickets_available': event.tickets.filter(status='available').count()
                }
            
            event_summaries.append(event_data)
        
        # Venue utilization (events managed)
        venue_stats = events.values('venue__name').annotate(
            events_count=Count('id'),
            total_bookings=Sum('bookings__id')
        )
        
        # Genre performance
        genre_performance = events.values(
            'artists__genre__name'
        ).annotate(
            event_count=Count('id'),
            avg_booking_percentage=Avg('tickets__status')  # This is simplified
        ).order_by('-event_count')[:5]
        
        return Response({
            'manager': {
                'name': user.get_full_name() or user.username,
                'email': user.email
            },
            'summary': {
                'total_events': events.count(),
                'total_revenue': round(total_revenue, 2),
                'total_bookings': total_bookings
            },
            'events': event_summaries,
            'venue_utilization': list(venue_stats),
            'top_genres': list(genre_performance)
        })