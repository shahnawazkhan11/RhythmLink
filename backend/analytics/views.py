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
        
        # Calculate real-time analytics from bookings
        from customers.models import Booking
        
        # Aggregate data for all events
        event_summaries = []
        total_revenue = 0
        total_bookings = 0
        
        for event in events:
            # Get real-time booking data
            event_bookings = Booking.objects.filter(
                event=event,
                status='confirmed'
            )
            
            event_revenue = event_bookings.aggregate(
                total=Sum('total_amount')
            )['total'] or 0
            
            event_booking_count = event_bookings.count()
            
            # Calculate booking percentage
            total_tickets = event.tickets.count()
            booked_tickets = event.tickets.filter(status='booked').count()
            booking_percentage = (booked_tickets / total_tickets * 100) if total_tickets > 0 else 0
            
            event_data = {
                'id': event.id,
                'name': event.name,
                'date': event.date,
                'venue': event.venue.name,
                'total_bookings': event_booking_count,
                'total_revenue': float(event_revenue),
                'booking_percentage': float(booking_percentage),
                'avg_rating': None,  # Can be calculated from feedback if needed
                'tickets_available': event.tickets.filter(status='available').count()
            }
            
            total_revenue += float(event_revenue)
            total_bookings += event_booking_count
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
        
        # Get upcoming events
        from datetime import date
        upcoming_events = events.filter(date__gte=date.today(), is_active=True).order_by('date')[:5]
        upcoming_events_data = [{
            'id': e.id,
            'name': e.name,
            'date': str(e.date),
            'start_time': str(e.start_time),
            'end_time': str(e.end_time),
            'venue_name': e.venue.name,
            'event_type_name': e.event_type.name if e.event_type else None,
            'ticket_price': str(e.ticket_price),
            'is_active': e.is_active
        } for e in upcoming_events]
        
        # Get top performing events (by revenue)
        top_performing = sorted(event_summaries, key=lambda x: x['total_revenue'], reverse=True)[:5]
        top_performing_events = [{
            'event': {
                'id': e['id'],
                'name': e['name'],
                'date': str(e['date'])
            },
            'revenue': str(e['total_revenue']),
            'tickets_sold': e['total_bookings']
        } for e in top_performing]
        
        # Get recent bookings
        from customers.models import Booking
        recent_bookings = Booking.objects.filter(
            event__in=events
        ).order_by('-booking_date')[:10]
        
        recent_bookings_data = [{
            'id': b.id,
            'customer': b.customer.id,
            'customer_name': b.customer.user.get_full_name() or b.customer.user.username,
            'event': b.event.id,
            'event_name': b.event.name,
            'total_amount': str(b.total_amount),
            'booking_date': b.booking_date.isoformat(),
            'status': b.status
        } for b in recent_bookings]
        
        return Response({
            'total_events': events.count(),
            'active_events': events.filter(is_active=True).count(),
            'total_revenue': str(round(total_revenue, 2)),
            'total_bookings': total_bookings,
            'upcoming_events': upcoming_events_data,
            'top_performing_events': top_performing_events,
            'recent_bookings': recent_bookings_data,
            'revenue_trend': [],  # Can be calculated if needed
        })