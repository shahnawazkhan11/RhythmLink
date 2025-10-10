from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time, timedelta
import random
from decimal import Decimal

from accounts.models import UserProfile
from artists.models import Genre, Artist
from events.models import EventType, Venue, Event, Performs, EventManager
from customers.models import Customer, Ticket, Booking, Feedback
from pricing.models import PriceTier
from pricing.services import DynamicPricingService


class Command(BaseCommand):
    help = 'Populate database with sample data for Phase 2 testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            # Clear in reverse dependency order
            Booking.objects.all().delete()
            Ticket.objects.all().delete()
            PriceTier.objects.all().delete()
            Performs.objects.all().delete()
            Event.objects.all().delete()
            Artist.objects.all().delete()
            Genre.objects.all().delete()
            Venue.objects.all().delete()
            EventType.objects.all().delete()
            Customer.objects.all().delete()
            EventManager.objects.all().delete()
            UserProfile.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()

        self.stdout.write('Creating sample data...')

        # Create genres
        genres = [
            'Rock', 'Pop', 'Hip Hop', 'Electronic', 'Classical',
            'Jazz', 'Country', 'R&B', 'Indie', 'Folk'
        ]
        genre_objects = []
        for genre_name in genres:
            genre, created = Genre.objects.get_or_create(
                name=genre_name,
                defaults={'description': f'{genre_name} music genre'}
            )
            genre_objects.append(genre)

        # Create artists
        artists_data = [
            ('Arijit Singh', 'Pop'), ('A.R. Rahman', 'Classical'),
            ('Divine', 'Hip Hop'), ('Prateek Kuhad', 'Indie'),
            ('Nucleya', 'Electronic'), ('Rahat Fateh Ali Khan', 'Classical'),
            ('Badshah', 'Hip Hop'), ('Shreya Ghoshal', 'Pop'),
            ('Anoushka Shankar', 'Classical'), ('Raja Kumari', 'Hip Hop')
        ]
        
        artist_objects = []
        for artist_name, genre_name in artists_data:
            genre = Genre.objects.get(name=genre_name)
            artist, created = Artist.objects.get_or_create(
                name=artist_name,
                defaults={
                    'genre': genre,
                    'contact_email': f'{artist_name.lower().replace(" ", "")}@email.com',
                    'bio': f'Renowned {genre_name} artist {artist_name}'
                }
            )
            artist_objects.append(artist)

        # Create event types
        event_types = ['Concert', 'Festival', 'Live Show', 'Album Launch', 'Tour']
        event_type_objects = []
        for event_type_name in event_types:
            event_type, created = EventType.objects.get_or_create(
                name=event_type_name,
                defaults={'description': f'{event_type_name} events'}
            )
            event_type_objects.append(event_type)

        # Create venues
        venues_data = [
            ('Phoenix MarketCity Arena', 'Mumbai', 5000),
            ('Jawaharlal Nehru Stadium', 'Delhi', 15000),
            ('KTPO Convention Centre', 'Bangalore', 3000),
            ('Nehru Indoor Stadium', 'Chennai', 8000),
            ('Shilpakala Vedika', 'Hyderabad', 2500),
            ('Nicco Park Amphitheater', 'Kolkata', 4000),
            ('Manekshaw Centre', 'Delhi', 1500),
            ('Phoenix Palassio', 'Lucknow', 2000),
        ]
        
        venue_objects = []
        for venue_name, city, capacity in venues_data:
            venue, created = Venue.objects.get_or_create(
                name=venue_name,
                defaults={
                    'location': f'{venue_name}, {city}',
                    'address': f'123 Main Street, {city}, India',
                    'city': city,
                    'state': 'Various',
                    'capacity': capacity,
                    'contact_email': f'info@{venue_name.lower().replace(" ", "")}.com'
                }
            )
            venue_objects.append(venue)

        # Create manager users
        manager_users = []
        for i in range(3):
            username = f'manager{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@rhythmlink.com',
                    'first_name': f'Manager{i+1}',
                    'last_name': 'Smith',
                    'is_staff': True
                }
            )
            if created:
                user.set_password('manager123')
                user.save()
            
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'manager', 'phone': f'9876543{i+10:03d}'}
            )
            
            event_manager, created = EventManager.objects.get_or_create(
                user=user,
                defaults={'contact_phone': f'9876543{i+10:03d}'}
            )
            
            manager_users.append(user)

        # Create customer users
        customer_users = []
        for i in range(20):
            username = f'customer{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@email.com',
                    'first_name': f'Customer{i+1}',
                    'last_name': 'Doe'
                }
            )
            if created:
                user.set_password('customer123')
                user.save()
            
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'customer', 'phone': f'9876543{i+100:03d}'}
            )
            
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={'phone': f'9876543{i+100:03d}'}
            )
            
            customer_users.append(user)

        # Create events
        event_names = [
            'Arijit Singh Live in Concert',
            'A.R. Rahman Symphony Night',
            'Divine Hip Hop Festival',
            'Prateek Kuhad Acoustic Evening',
            'Nucleya Electronic Night',
            'Rahat Fateh Ali Khan Sufi Night',
            'Badshah Live Performance',
            'Shreya Ghoshal Classical Evening',
        ]
        
        events = []
        base_date = date.today() + timedelta(days=30)
        
        for i, event_name in enumerate(event_names):
            event_date = base_date + timedelta(days=i*7)
            venue = random.choice(venue_objects)
            event_type = random.choice(event_type_objects)
            base_price = random.choice([500, 750, 1000, 1250, 1500])
            manager = random.choice(manager_users)
            
            event, created = Event.objects.get_or_create(
                name=event_name,
                defaults={
                    'description': f'An amazing {event_type.name.lower()} featuring {event_name}',
                    'date': event_date,
                    'start_time': time(19, 0),  # 7 PM
                    'end_time': time(22, 0),    # 10 PM
                    'venue': venue,
                    'event_type': event_type,
                    'ticket_price': Decimal(str(base_price))
                }
            )
            
            if created:
                # Assign artist to event
                artist = random.choice(artist_objects)
                Performs.objects.create(
                    artist=artist,
                    event=event,
                    performance_time=time(20, 0),  # 8 PM
                    duration_minutes=120,
                    is_headliner=True
                )
                
                # Assign manager to event
                event_manager = EventManager.objects.get(user=manager)
                event_manager.managed_events.add(event)
                
                # Create price tiers using service
                DynamicPricingService.create_default_price_tiers(
                    event, manager, Decimal(str(base_price))
                )
                
                # Create tickets for the event
                ticket_count = min(venue.capacity, 200)  # Limit for demo
                for seat_num in range(1, ticket_count + 1):
                    current_tier = DynamicPricingService.calculate_current_tier(event)
                    price = current_tier.price if current_tier else Decimal(str(base_price))
                    
                    Ticket.objects.create(
                        event=event,
                        seat_number=f'A-{seat_num:03d}',
                        section='General',
                        base_price=Decimal(str(base_price)),
                        final_price=price,
                        current_tier=current_tier
                    )
                
                events.append(event)

        # Create some bookings to simulate demand
        for event in events:
            # Random bookings (10-40% of capacity)
            booking_percentage = random.uniform(10, 40)
            tickets_to_book = int(event.tickets.count() * booking_percentage / 100)
            
            available_tickets = list(event.tickets.filter(status='available')[:tickets_to_book])
            
            for i, ticket in enumerate(available_tickets):
                customer = random.choice(customer_users).customer_profile
                
                booking = Booking.objects.create(
                    customer=customer,
                    event=event,
                    total_amount=ticket.final_price,
                    status='confirmed'
                )
                
                booking.tickets.add(ticket)
                ticket.status = 'booked'
                ticket.save()
                
                # Create some feedback (70% chance)
                if random.random() < 0.7:
                    Feedback.objects.create(
                        customer=customer,
                        event=event,
                        booking=booking,
                        rating=random.randint(3, 5),
                        comment=f'Great event! Really enjoyed the performance.',
                        would_recommend=True
                    )
            
            # Update pricing after bookings
            DynamicPricingService.update_ticket_prices(event)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {Genre.objects.count()} genres\n'
                f'- {Artist.objects.count()} artists\n'
                f'- {Venue.objects.count()} venues\n'
                f'- {Event.objects.count()} events\n'
                f'- {User.objects.filter(profile__role="manager").count()} managers\n'
                f'- {User.objects.filter(profile__role="customer").count()} customers\n'
                f'- {Ticket.objects.count()} tickets\n'
                f'- {Booking.objects.count()} bookings\n'
                f'- {PriceTier.objects.count()} price tiers'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                '\nLogin credentials:\n'
                'Managers: manager1/manager123, manager2/manager123, manager3/manager123\n'
                'Customers: customer1/customer123, customer2/customer123, etc.\n'
                'Admin panel: /admin/'
            )
        )