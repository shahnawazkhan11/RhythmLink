"""
Django management command to import all data from Excel files
Usage: python manage.py import_all_data
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
    help = 'Import all data from Excel files in the data directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default='data',
            help='Directory containing Excel files (default: data/)'
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
        """Import artists from Artists.xlsx"""
        file_path = os.path.join(data_dir, 'Artists.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Artists - file not found: {file_path}'))
            return

        self.stdout.write('Importing Artists...')
        # Try reading as CSV first (files have .xlsx extension but are CSV)
        try:
            df = pd.read_csv(file_path)
        except:
            df = pd.read_excel(file_path, engine='openpyxl')
        
        artists_created = 0
        genres_created = set()

        for idx, row in df.iterrows():
            try:
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

                # Create artist
                artist_name = str(row.get('name', f'Artist_{idx}')).strip()
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

                if created:
                    artists_created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error importing artist at row {idx}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {artists_created} artists and {len(genres_created)} genres'))

    def import_albums(self, data_dir):
        """Import albums from Albums.xlsx"""
        file_path = os.path.join(data_dir, 'Albums.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Albums - file not found: {file_path}'))
            return

        self.stdout.write('Importing Albums...')
        # Try reading as CSV first (files have .xlsx extension but are CSV)
        try:
            df = pd.read_csv(file_path)
        except:
            df = pd.read_excel(file_path, engine='openpyxl')
        
        albums_created = 0
        # Create a mapping of artist_id to Artist objects
        artists_map = {}

        for idx, row in df.iterrows():
            try:
                artist_id = str(row.get('artist_id', '')).strip()
                album_name = str(row.get('album_name', '')).strip()
                
                if not album_name or album_name == 'nan':
                    continue

                # Find artist by artist_id if we have a mapping, otherwise skip
                if artist_id not in artists_map:
                    # We don't have artist names in Albums.xlsx, so we'll need to create a placeholder
                    # or skip this album. Let's create with first available artist or skip.
                    artist = Artist.objects.first()
                    if not artist:
                        continue
                    artists_map[artist_id] = artist
                else:
                    artist = artists_map[artist_id]

                # Parse release date
                release_date_raw = row.get('release_date')
                if pd.notna(release_date_raw):
                    if isinstance(release_date_raw, str):
                        try:
                            release_date = datetime.strptime(release_date_raw, '%Y-%m-%d').date()
                        except ValueError:
                            try:
                                release_date = datetime.strptime(release_date_raw, '%m/%d/%Y').date()
                            except ValueError:
                                release_date = timezone.now().date()
                    else:
                        release_date = pd.to_datetime(release_date_raw).date()
                else:
                    release_date = timezone.now().date()

                total_tracks = 0  # Will be counted from Track imports

                album, created = Album.objects.get_or_create(
                    artist=artist,
                    album_name=album_name,
                    defaults={
                        'release_date': release_date,
                        'total_tracks': total_tracks,
                        'spotify_url': str(row.get('spotify_url', '')).strip() if pd.notna(row.get('spotify_url')) else ''
                    }
                )

                if created:
                    albums_created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error importing album at row {idx}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {albums_created} albums'))

    def import_tracks(self, data_dir):
        """Import tracks from Tracks.xlsx"""
        file_path = os.path.join(data_dir, 'Tracks.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Tracks - file not found: {file_path}'))
            return

        self.stdout.write('Importing Tracks...')
        # Try reading as CSV first (files have .xlsx extension but are CSV)
        try:
            df = pd.read_csv(file_path)
        except:
            df = pd.read_excel(file_path, engine='openpyxl')
        
        tracks_created = 0

        for idx, row in df.iterrows():
            try:
                artist_name = str(row.get('Artist_Name', '')).strip()
                album_name = str(row.get('Album_Name', '')).strip()
                track_name = str(row.get('Track_Name', '')).strip()
                
                if not all([artist_name, album_name, track_name]) or \
                   any(x == 'nan' for x in [artist_name, album_name, track_name]):
                    continue

                # Find the album
                try:
                    artist = Artist.objects.get(name=artist_name)
                    album = Album.objects.get(artist=artist, album_name=album_name)
                except (Artist.DoesNotExist, Album.DoesNotExist):
                    self.stdout.write(self.style.WARNING(
                        f'  ! Album not found: {album_name} by {artist_name}'
                    ))
                    continue

                track_number = int(row.get('Track_Number', 1)) if pd.notna(row.get('Track_Number')) else 1
                duration_ms = int(row.get('Duration_ms', 180000)) if pd.notna(row.get('Duration_ms')) else 180000

                track, created = Track.objects.get_or_create(
                    album=album,
                    track_number=track_number,
                    track_name=track_name,
                    defaults={
                        'duration_ms': duration_ms
                    }
                )

                if created:
                    tracks_created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error importing track at row {idx}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {tracks_created} tracks'))

    def import_fans(self, data_dir):
        """Import fans/customers from Fans.xlsx"""
        file_path = os.path.join(data_dir, 'Fans.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Fans - file not found: {file_path}'))
            return

        self.stdout.write('Importing Fans...')
        # Try reading as CSV first (files have .xlsx extension but are CSV)
        try:
            df = pd.read_csv(file_path)
        except:
            df = pd.read_excel(file_path, engine='openpyxl')
        
        fans_created = 0

        for idx, row in df.iterrows():
            try:
                fan_id = str(row.get('Fan_ID', f'fan_{idx}')).strip()
                name = str(row.get('Name', f'Fan {idx}')).strip()
                email = str(row.get('Email', f'fan{idx}@example.com')).strip()
                country = str(row.get('Country', '')).strip()
                
                # Create username from email or fan_id
                username = email.split('@')[0] if '@' in email else f'fan_{idx}'
                
                # Create or get user
                user, user_created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': email,
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

                if created:
                    fans_created += 1

                # Handle preferred genres if present
                preferred_genre = str(row.get('Preferred_Genre', '')).strip()
                if preferred_genre and preferred_genre != 'nan':
                    try:
                        genre = Genre.objects.get(name=preferred_genre)
                        customer.preferred_genres.add(genre)
                    except Genre.DoesNotExist:
                        pass

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error importing fan at row {idx}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {fans_created} fans'))

    def import_events(self, data_dir):
        """Import events from Events.xlsx"""
        file_path = os.path.join(data_dir, 'Events.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'  ! Skipping Events - file not found: {file_path}'))
            return

        self.stdout.write('Importing Events...')
        # Try reading as CSV first (files have .xlsx extension but are CSV)
        try:
            df = pd.read_csv(file_path)
        except:
            df = pd.read_excel(file_path, engine='openpyxl')
        
        events_created = 0
        venues_created = 0

        for idx, row in df.iterrows():
            try:
                event_name = str(row.get('Event_Name', f'Event {idx}')).strip()
                venue_name = str(row.get('Venue', 'Unknown Venue')).strip()
                location = str(row.get('Location', 'Unknown Location')).strip()
                artist_name = str(row.get('Artist_Name', '')).strip()
                
                # Parse date
                event_date_raw = row.get('Date')
                if pd.notna(event_date_raw):
                    if isinstance(event_date_raw, str):
                        try:
                            event_date = datetime.strptime(event_date_raw, '%Y-%m-%d').date()
                        except ValueError:
                            try:
                                event_date = datetime.strptime(event_date_raw, '%m/%d/%Y').date()
                            except ValueError:
                                event_date = timezone.now().date()
                    else:
                        event_date = pd.to_datetime(event_date_raw).date()
                else:
                    event_date = timezone.now().date()

                # Parse time
                time_str = str(row.get('Time', '20:00')).strip()
                try:
                    if ':' in time_str:
                        hour, minute = time_str.split(':')[:2]
                        start_time = time(int(hour), int(minute))
                    else:
                        start_time = time(20, 0)
                except:
                    start_time = time(20, 0)

                end_time = time((start_time.hour + 2) % 24, start_time.minute)

                # Create or get event type
                event_type, _ = EventType.objects.get_or_create(
                    name='Concert',
                    defaults={'description': 'Live concert performance'}
                )

                # Create or get venue
                venue, venue_created = Venue.objects.get_or_create(
                    name=venue_name,
                    defaults={
                        'location': location,
                        'address': location,
                        'city': location.split(',')[0] if ',' in location else location,
                        'state': location.split(',')[-1].strip() if ',' in location else 'Unknown',
                        'capacity': 5000
                    }
                )

                if venue_created:
                    venues_created += 1

                # Get ticket price
                ticket_price = row.get('Ticket_Price', 50.00)
                if pd.notna(ticket_price):
                    ticket_price = Decimal(str(ticket_price))
                else:
                    ticket_price = Decimal('50.00')

                # Create event
                event, created = Event.objects.get_or_create(
                    name=event_name,
                    date=event_date,
                    venue=venue,
                    defaults={
                        'description': f'{event_name} at {venue_name}',
                        'start_time': start_time,
                        'end_time': end_time,
                        'event_type': event_type,
                        'ticket_price': ticket_price,
                        'is_active': True
                    }
                )

                if created:
                    events_created += 1

                    # Link artist to event if specified
                    if artist_name and artist_name != 'nan':
                        try:
                            artist = Artist.objects.get(name=artist_name)
                            Performs.objects.get_or_create(
                                artist=artist,
                                event=event,
                                defaults={
                                    'performance_time': start_time,
                                    'duration_minutes': 90,
                                    'is_headliner': True
                                }
                            )
                        except Artist.DoesNotExist:
                            pass

                    # Create some sample tickets for the event
                    self.create_sample_tickets(event, venue.capacity)

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ! Error importing event at row {idx}: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(
            f'  ✓ Imported {events_created} events and {venues_created} venues'
        ))

    def create_sample_tickets(self, event, capacity):
        """Create sample tickets for an event"""
        # Create a reasonable number of tickets (max 100 for sample)
        num_tickets = min(100, capacity)
        
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
        """Import fan interactions from Fan_interactions.xlsx"""
        file_path = os.path.join(data_dir, 'Fan_interactions.xlsx')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(
                f'  ! Skipping Fan Interactions - file not found: {file_path}'
            ))
            return

        self.stdout.write('Importing Fan Interactions...')
        # Try reading as CSV first (files have .xlsx extension but are CSV)
        try:
            df = pd.read_csv(file_path)
        except:
            df = pd.read_excel(file_path, engine='openpyxl')
        
        interactions_created = 0

        for idx, row in df.iterrows():
            try:
                fan_id = str(row.get('Fan_ID', '')).strip()
                track_name = str(row.get('Track_Name', '')).strip()
                interaction_type = str(row.get('Interaction_Type', 'play')).strip().lower()
                
                if not all([fan_id, track_name]) or any(x == 'nan' for x in [fan_id, track_name]):
                    continue

                # Map interaction type to valid choices
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
                interaction_type = type_mapping.get(interaction_type, 'play')

                # Find the fan
                try:
                    username = fan_id.split('@')[0] if '@' in fan_id else fan_id
                    user = User.objects.get(username__icontains=username[:30])
                    customer = Customer.objects.get(user=user)
                except (User.DoesNotExist, Customer.DoesNotExist):
                    # Try by email if fan_id looks like an email
                    if '@' in fan_id:
                        try:
                            user = User.objects.get(email=fan_id)
                            customer = Customer.objects.get(user=user)
                        except (User.DoesNotExist, Customer.DoesNotExist):
                            continue
                    else:
                        continue

                # Find the track
                try:
                    track = Track.objects.filter(track_name__icontains=track_name).first()
                    if not track:
                        continue
                except Track.DoesNotExist:
                    continue

                # Parse timestamp
                timestamp_raw = row.get('Timestamp')
                if pd.notna(timestamp_raw):
                    if isinstance(timestamp_raw, str):
                        try:
                            timestamp = datetime.strptime(timestamp_raw, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            try:
                                timestamp = datetime.strptime(timestamp_raw, '%m/%d/%Y %H:%M')
                            except ValueError:
                                timestamp = timezone.now()
                    else:
                        timestamp = pd.to_datetime(timestamp_raw)
                    
                    # Make timezone aware
                    if timezone.is_naive(timestamp):
                        timestamp = timezone.make_aware(timestamp)
                else:
                    timestamp = timezone.now()

                # Create interaction
                interaction, created = FanInteraction.objects.get_or_create(
                    fan=customer,
                    track=track,
                    timestamp=timestamp,
                    interaction_type=interaction_type,
                    defaults={
                        'device_type': str(row.get('Device', 'web')).strip() if pd.notna(row.get('Device')) else 'web',
                        'location': str(row.get('Location', '')).strip() if pd.notna(row.get('Location')) else ''
                    }
                )

                if created:
                    interactions_created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(
                    f'  ! Error importing interaction at row {idx}: {str(e)}'
                ))
                continue

        self.stdout.write(self.style.SUCCESS(f'  ✓ Imported {interactions_created} fan interactions'))
