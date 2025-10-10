from django.core.management.base import BaseCommand
from django.db.models import Sum, Avg, Count
from decimal import Decimal
from events.models import Event
from analytics.models import EventAnalytics


class Command(BaseCommand):
    help = 'Refresh analytics data for all events'

    def handle(self, *args, **options):
        self.stdout.write('Refreshing event analytics...')
        
        events = Event.objects.all()
        updated_count = 0
        
        for event in events:
            # Calculate analytics
            tickets = event.tickets.all()
            bookings = event.bookings.all()
            feedback = event.feedback.all()
            
            total_tickets = tickets.count()
            booked_tickets = tickets.filter(status='booked').count()
            
            total_bookings = bookings.filter(status__in=['confirmed', 'pending']).count()
            total_revenue = bookings.filter(status='confirmed').aggregate(
                total=Sum('total_amount')
            )['total'] or Decimal('0.00')
            
            avg_rating = feedback.aggregate(avg=Avg('rating'))['avg']
            
            booking_percentage = (booked_tickets / total_tickets * 100) if total_tickets > 0 else 0
            tickets_available = tickets.filter(status='available').count()
            
            # Update or create analytics record
            analytics, created = EventAnalytics.objects.update_or_create(
                event=event,
                defaults={
                    'total_bookings': total_bookings,
                    'total_revenue': total_revenue,
                    'avg_rating': avg_rating,
                    'booking_percentage': Decimal(str(booking_percentage)),
                    'tickets_available': tickets_available
                }
            )
            
            updated_count += 1
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} analytics for: {event.name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully refreshed analytics for {updated_count} events')
        )