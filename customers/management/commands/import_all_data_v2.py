"""
Django management command to import all data from CSV files (with .xlsx extension)
Usage: python manage.py import_all_data_v2
"""
import os
import pandas as pd
from datetime import datetime, time
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from artists.models import Genre, Artist, Album, Track
from events.models import EventType, Venue, Event, Performs
from customers.models import Customer, Ticket, Booking, Feedback, FanInteraction


class Command(BaseCommand):
    help = 'Import all data from CSV files in the data directory'

    def __init__(self):
        super().__init__()
        # Mappings for IDs to Django objects
        self.artist_map = {}  # artist_id -> Artist object
        self.album_map = {}   # album_id -> Album object
        self.track_map = {}   # track_id -> Track object
        self.fan_map = {}     # fan_id -> Customer object

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default='data',
            help='Directory containing CSV files (default: data/)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import'
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        clear_data = options['clear']

        # Verify data directory exists
        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f'Data directory not found: {data_dir}'))
            return

        self.stdout.write(self.style.SUCCESS('Starting data import...'))

        try:
            with transaction.atomic():
                if clear_data:
                    self.stdout.write(self.style.WARNING('Clearing existing data...'))
                    self.clear_all_data()

                # Import in order of dependencies
                self.import_artists(data_dir)
                self.import_albums(data_dir)
                self.import_tracks(data_dir)
                self.import_fans(data_dir)
                self.import_events(data_dir)
                self.import_fan_interactions(data_dir)

            self.stdout.write(self.style.SUCCESS('✓ All data imported successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during import: {str(e)}'))
            import traceback
            traceback.print_exc()
            raise

    def clear_all_data(self):
        """Clear all data from the database"""
        FanInteraction.objects.all().delete()
        Feedback.objects.all().delete()
        Booking.objects.all().delete()
        Ticket.objects.all().delete()
        Performs.objects.all().delete()
        Event.objects.all().delete()
        Venue.objects.all().delete()
        EventType.objects.all().delete()
        Track.objects.all().delete()
        Album.objects.all().delete()
        Artist.objects.all().delete()
        Genre.objects.all().delete()
        Customer.objects.all().delete()
        # Note: Not deleting User objects to preserve admin/staff accounts
        self.stdout.write(self.style.WARNING('  ✓ Cleared existing data'))

    def import_artists(self, data_dir):
        """Import artists from Artists.xlsx (CSV file)"""
        file_path = os.path.join(data_dir, 'Artists.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Artists - file not found'))
            return

        self.stdout.write('Importing Artists...')
        df = pd.read_csv(file_path)
        
        artists_created = 0
        genres_created = set()

        for idx, row in df.iterrows():
            try:
                artist_id = str(row.get('artist_id', '')).strip()
                artist_name = str(row.get('name', f'Artist_{idx}')).strip()
                
                # Get genres from the 'genres' column (comma-separated)
                genres_str = str(row.get('genres', 'Unknown')).strip()
                genre_names = [g.strip() for g in genres_str.split(',')] if genres_str and genres_str != 'nan' else ['Unknown']
                
                # Use the first genre as the primary genre
                genre_name = genre_names[0] if genre_names else 'Unknown'
                genre, created = Genre.objects.get_or_create(
                    name=genre_name,
                    defaults={'description': f'{genre_name} music genre'}
                )
                if created:
                    genres_created.add(genre_name)

                followers = int(row.get('followers', 0)) if pd.notna(row.get('followers')) else 0
                popularity = int(row.get('popularity', 0)) if pd.notna(row.get('popularity')) else 0

                artist, created = Artist.objects.get_or_create(
                    name=artist_name,
                    defaults={
                        'genre': genre,
                        'followers': followers,
                        'popularity': popularity,
                        'is_active': True
                    }
                )

                # Store in mapping
                if artist_id:
                    self.artist_map[artist_id] = artist

                if created:
                    artists_created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error at row {idx}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {artists_created} artists and {len(genres_created)} genres'))

    def import_albums(self, data_dir):
        """Import albums from Albums.xlsx (CSV file)"""
        file_path = os.path.join(data_dir, 'Albums.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Albums - file not found'))
            return

        self.stdout.write('Importing Albums...')
        df = pd.read_csv(file_path)
        
        albums_created = 0

        for idx, row in df.iterrows():
            try:
                album_id = str(row.get('album_id', '')).strip()
                artist_id = str(row.get('artist_id', '')).strip()
                album_name = str(row.get('album_name', '')).strip()
                
                if not album_name or album_name == 'nan':
                    continue

                # Find artist by artist_id
                artist = self.artist_map.get(artist_id)
                if not artist:
                    # Try to find any artist as fallback
                    artist = Artist.objects.first()
                    if not artist:
                        continue

                # Parse release date
                release_date_raw = row.get('release_date')
                if pd.notna(release_date_raw):
                    try:
                        release_date = pd.to_datetime(release_date_raw).date()
                    except:
                        release_date = timezone.now().date()
                else:
                    release_date = timezone.now().date()

                spotify_url = str(row.get('spotify_url', '')).strip() if pd.notna(row.get('spotify_url')) else ''

                album, created = Album.objects.get_or_create(
                    artist=artist,
                    album_name=album_name,
                    defaults={
                        'release_date': release_date,
                        'total_tracks': 0,  # Will be updated when importing tracks
                        'spotify_url': spotify_url
                    }
                )

                # Store in mapping
                if album_id:
                    self.album_map[album_id] = album

                if created:
                    albums_created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error at row {idx}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {albums_created} albums'))

    def import_tracks(self, data_dir):
        """Import tracks from Tracks.xlsx (CSV file)"""
        file_path = os.path.join(data_dir, 'Tracks.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Tracks - file not found'))
            return

        self.stdout.write('Importing Tracks...')
        df = pd.read_csv(file_path)
        
        tracks_created = 0

        for idx, row in df.iterrows():
            try:
                track_id = str(row.get('track_id', '')).strip()
                album_id = str(row.get('album_id', '')).strip()
                track_name = str(row.get('track_name', '')).strip()
                
                if not track_name or track_name == 'nan':
                    continue

                # Find album by album_id
                album = self.album_map.get(album_id)
                if not album:
                    continue

                track_number = int(row.get('track_number', 1)) if pd.notna(row.get('track_number')) else 1
                duration_ms = int(row.get('duration_ms', 180000)) if pd.notna(row.get('duration_ms')) else 180000

                track, created = Track.objects.get_or_create(
                    album=album,
                    track_number=track_number,
                    defaults={
                        'track_name': track_name,
                        'duration_ms': duration_ms
                    }
                )

                # Store in mapping
                if track_id:
                    self.track_map[track_id] = track

                if created:
                    tracks_created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error at row {idx}: {str(e)}'))
                continue

        # Update album total_tracks
        for album in Album.objects.all():
            album.total_tracks = album.tracks.count()
            album.save(update_fields=['total_tracks'])

        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {tracks_created} tracks'))

    def import_fans(self, data_dir):
        """Import fans/customers from Fans.xlsx (CSV file)"""
        file_path = os.path.join(data_dir, 'Fans.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Fans - file not found'))
            return

        self.stdout.write('Importing Fans...')
        df = pd.read_csv(file_path)
        
        fans_created = 0

        for idx, row in df.iterrows():
            try:
                fan_id = str(row.get('fan_id', f'fan_{idx}')).strip()
                name = str(row.get('name', f'Fan {idx}')).strip()
                email = str(row.get('email', f'fan{idx}@example.com')).strip()
                country = str(row.get('country', '')).strip()
                
                # Create username from email or fan_id
                username = email.split('@')[0][:30] if '@' in email else f'fan_{idx}'
                # Make username unique
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                # Create or get user
                user, user_created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'username': username,
                        'first_name': name.split()[0] if name else 'Fan',
                        'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
                    }
                )

                # Create customer profile
                customer, created = Customer.objects.get_or_create(
                    user=user,
                    defaults={
                        'country': country if country and country != 'nan' else '',
                        'marketing_consent': True
                    }
                )

                # Store in mapping
                if fan_id:
                    self.fan_map[fan_id] = customer

                if created:
                    fans_created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error at row {idx}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {fans_created} fans'))

    def import_events(self, data_dir):
        """Import events from Events.xlsx (CSV file)"""
        file_path = os.path.join(data_dir, 'Events.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Events - file not found'))
            return

        self.stdout.write('Importing Events...')
        df = pd.read_csv(file_path)
        
        events_created = 0
        venues_created = 0

        for idx, row in df.iterrows():
            try:
                event_name = str(row.get('name', f'Event {idx}')).strip()
                location = str(row.get('location', 'Unknown Location')).strip()
                artist_id = str(row.get('artist_id', '')).strip()
                revenue = row.get('revenue', 0)
                
                # Parse date
                event_date_raw = row.get('date')
                if pd.notna(event_date_raw):
                    try:
                        event_date = pd.to_datetime(event_date_raw).date()
                    except:
                        event_date = timezone.now().date()
                else:
                    event_date = timezone.now().date()

                # Create default times
                start_time = time(20, 0)
                end_time = time(23, 0)

                # Create or get event type
                event_type, _ = EventType.objects.get_or_create(
                    name='Concert',
                    defaults={'description': 'Live concert performance'}
                )

                # Create or get venue
                city = location.split(',')[0] if ',' in location else location
                venue, venue_created = Venue.objects.get_or_create(
                    name=f'Venue - {city}',
                    defaults={
                        'location': location,
                        'address': location,
                        'city': city,
                        'state': location.split(',')[-1].strip() if ',' in location else 'Unknown',
                        'capacity': 5000
                    }
                )

                if venue_created:
                    venues_created += 1

                # Calculate ticket price from revenue (rough estimate)
                ticket_price = Decimal('50.00')
                if pd.notna(revenue) and revenue > 0:
                    # Assume 100 tickets sold on average
                    ticket_price = Decimal(str(min(revenue / 100, 500)))

                # Create event
                event, created = Event.objects.get_or_create(
                    name=event_name,
                    date=event_date,
                    venue=venue,
                    defaults={
                        'description': f'{event_name} at {location}',
                        'start_time': start_time,
                        'end_time': end_time,
                        'event_type': event_type,
                        'ticket_price': ticket_price,
                        'is_active': event_date >= timezone.now().date()
                    }
                )

                if created:
                    events_created += 1

                    # Link artist to event if specified
                    artist = self.artist_map.get(artist_id)
                    if artist:
                        Performs.objects.get_or_create(
                            artist=artist,
                            event=event,
                            defaults={
                                'performance_time': start_time,
                                'duration_minutes': 90,
                                'is_headliner': True
                            }
                        )

                    # Create some sample tickets for the event
                    self.create_sample_tickets(event, min(50, venue.capacity))

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error at row {idx}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Imported {events_created} events and {venues_created} venues'
        ))

    def create_sample_tickets(self, event, num_tickets):
        """Create sample tickets for an event"""
        for i in range(1, num_tickets + 1):
            section = f"Section {chr(65 + (i // 20))}"  # A, B, C, etc.
            seat_number = f"{section}-{i}"
            
            Ticket.objects.create(
                event=event,
                seat_number=seat_number,
                section=section,
                base_price=event.ticket_price,
                final_price=event.ticket_price,
                status='available'
            )

    def import_fan_interactions(self, data_dir):
        """Import fan interactions from Fan_interactions.xlsx (CSV file)"""
        file_path = os.path.join(data_dir, 'Fan_interactions.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Fan Interactions - file not found'))
            return

        self.stdout.write('Importing Fan Interactions...')
        df = pd.read_csv(file_path)
        
        interactions_created = 0

        # Map interaction types
        type_mapping = {
            'play': 'play',
            'stream': 'play',
            'listen': 'play',
            'like': 'like',
            'favorite': 'like',
            'share': 'share',
            'playlist': 'playlist_add',
            'playlist_add': 'playlist_add',
            'download': 'download'
        }

        for idx, row in df.iterrows():
            try:
                fan_id = str(row.get('fan_id', '')).strip()
                track_id = str(row.get('track_id', '')).strip()
                interaction_type = str(row.get('type_of_interaction', 'play')).strip().lower()
                
                # Get fan and track from mappings
                customer = self.fan_map.get(fan_id)
                track = self.track_map.get(track_id)
                
                if not customer or not track:
                    continue

                # Map interaction type
                interaction_type = type_mapping.get(interaction_type, 'play')

                # Parse timestamp
                timestamp_raw = row.get('timestamp')
                if pd.notna(timestamp_raw):
                    try:
                        timestamp = pd.to_datetime(timestamp_raw)
                        # Make timezone aware
                        if timezone.is_naive(timestamp):
                            timestamp = timezone.make_aware(timestamp)
                    except:
                        timestamp = timezone.now()
                else:
                    timestamp = timezone.now()

                # Create interaction
                interaction, created = FanInteraction.objects.get_or_create(
                    fan=customer,
                    track=track,
                    timestamp=timestamp,
                    interaction_type=interaction_type,
                    defaults={
                        'device_type': 'web',
                        'location': customer.country
                    }
                )

                if created:
                    interactions_created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error at row {idx}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {interactions_created} fan interactions'))
