# Management command to create tickets for events
from django.core.management.base import BaseCommand
from events.models import Event
from customers.models import Ticket


class Command(BaseCommand):
    help = 'Create tickets for events that don\'t have tickets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--event-id',
            type=int,
            help='Specific event ID to create tickets for',
        )
        parser.add_argument(
            '--tickets-per-event',
            type=int,
            default=100,
            help='Number of tickets to create per event (default: 100)',
        )

    def handle(self, *args, **options):
        event_id = options.get('event_id')
        tickets_per_event = options.get('tickets_per_event')

        if event_id:
            events = Event.objects.filter(id=event_id, is_active=True)
        else:
            events = Event.objects.filter(is_active=True)

        if not events.exists():
            self.stdout.write(self.style.WARNING('No active events found'))
            return

        total_created = 0

        for event in events:
            existing_tickets = event.tickets.count()
            
            if existing_tickets >= tickets_per_event:
                self.stdout.write(
                    self.style.SUCCESS(f'Event "{event.name}" already has {existing_tickets} tickets')
                )
                continue

            tickets_to_create = tickets_per_event - existing_tickets
            created_count = 0

            # Create tickets
            for i in range(tickets_to_create):
                seat_number = f"SEAT-{existing_tickets + i + 1:04d}"
                section = f"Section-{((existing_tickets + i) // 25) + 1}"
                
                Ticket.objects.create(
                    event=event,
                    seat_number=seat_number,
                    section=section,
                    base_price=event.ticket_price,
                    final_price=event.ticket_price,
                    status='available'
                )
                created_count += 1

            total_created += created_count
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {created_count} tickets for event "{event.name}" '
                    f'(Total: {existing_tickets + created_count})'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal tickets created: {total_created}')
        )
