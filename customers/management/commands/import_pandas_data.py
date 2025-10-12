"""
Import data from Excel files using pandas (supports both .xls and .xlsx)
"""
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from datetime import datetime, date

from artists.models import Genre, Artist, Album, Track
from events.models import Event, Venue, EventType, Performs
from customers.models import Customer, Booking, Ticket, FanInteraction


class Command(BaseCommand):
    help = 'Import data from Excel files using pandas'

    def add_arguments(self, parser):
        parser.add_argument('--folder', type=str, default='data', help='Folder containing Excel files')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before import')

    def handle(self, *args, **options):
        folder = options['folder']
        clear_data = options['clear']
        
        if clear_data:
            self.stdout.write(self.style.WARNING('[!] Clearing existing data...'))
            self.clear_all_data()
        
        self.stdout.write(self.style.SUCCESS('[*] Starting Excel data import...'))
        
        try:
            # Import in dependency order
            self.import_artists(f'{folder}/Artists.xlsx')
            self.import_albums(f'{folder}/Albums.xlsx')
            self.import_tracks(f'{folder}/Tracks.xlsx')
            self.import_fans(f'{folder}/Fans.xlsx')
            self.import_events(f'{folder}/Events.xlsx')
            self.import_fan_interactions(f'{folder}/Fan_interactions.xlsx')
            
            self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Excel import complete!'))
            self.print_summary()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n[ERROR] Import failed: {str(e)}'))
            import traceback
            traceback.print_exc()
            raise

    def clear_all_data(self):
        """Clear all existing data"""
        FanInteraction.objects.all().delete()
        Booking.objects.all().delete()
        Ticket.objects.all().delete()
        Track.objects.all().delete()
        Album.objects.all().delete()
        Performs.objects.all().delete()
        Event.objects.all().delete()
        Customer.objects.all().delete()
        Artist.objects.all().delete()
        Genre.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('  [+] Data cleared')

    @transaction.atomic
    def import_artists(self, file_path):
        """Import artists from Excel"""
        self.stdout.write('\n[*] Importing artists...')
        
        # Try openpyxl first, fallback to xlrd for old .xls format
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except:
            df = pd.read_excel(file_path, engine='xlrd')
        
        for _, row in df.iterrows():
            # Get or create genre
            genre_name = str(row.get('genres', 'Unknown')).strip()
            genre, _ = Genre.objects.get_or_create(name=genre_name)
            
            # Create artist
            artist, created = Artist.objects.update_or_create(
                name=str(row['name']).strip(),
                defaults={
                    'genre': genre,
                    'followers': int(row.get('followers', 0)) if pd.notna(row.get('followers')) else 0,
                    'popularity': int(row.get('popularity', 0)) if pd.notna(row.get('popularity')) else 0,
                }
            )
            
            if created:
                self.stdout.write(f'  [+] Created artist: {artist.name}')
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] Imported {Artist.objects.count()} artists'))

    @transaction.atomic
    def import_albums(self, file_path):
        """Import albums from Excel"""
        self.stdout.write('\n[*] Importing albums...')
        
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except:
            df = pd.read_excel(file_path, engine='xlrd')
        
        for _, row in df.iterrows():
            artist_id = row.get('artist_id')
            try:
                artist = Artist.objects.all()[int(artist_id) - 1] if pd.notna(artist_id) else None
            except (IndexError, ValueError):
                self.stdout.write(self.style.WARNING(f'  [!] Artist ID {artist_id} not found'))
                continue
            
            release_date = pd.to_datetime(row.get('release_date')).date() if pd.notna(row.get('release_date')) else timezone.now().date()
            
            album, created = Album.objects.update_or_create(
                artist=artist,
                album_name=str(row['album_name']).strip(),
                defaults={
                    'release_date': release_date,
                    'total_tracks': int(row.get('total_tracks', 0)) if pd.notna(row.get('total_tracks')) else 0,
                }
            )
            
            if created:
                self.stdout.write(f'  [+] Created album: {album.album_name}')
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] Imported {Album.objects.count()} albums'))

    @transaction.atomic
    def import_tracks(self, file_path):
        """Import tracks from Excel"""
        self.stdout.write('\n[*] Importing tracks...')
        
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except:
            df = pd.read_excel(file_path, engine='xlrd')
        
        for _, row in df.iterrows():
            album_id = row.get('album_id')
            try:
                album = Album.objects.all()[int(album_id) - 1] if pd.notna(album_id) else None
            except (IndexError, ValueError):
                self.stdout.write(self.style.WARNING(f'  [!] Album ID {album_id} not found'))
                continue
            
            track, created = Track.objects.update_or_create(
                album=album,
                track_number=int(row.get('track_number', 1)),
                defaults={
                    'track_name': str(row['track_name']).strip(),
                    'duration_ms': int(row.get('duration_ms', 0)) if pd.notna(row.get('duration_ms')) else 0,
                }
            )
            
            if created:
                self.stdout.write(f'  [+] Created track: {track.track_name}')
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] Imported {Track.objects.count()} tracks'))

    @transaction.atomic
    def import_fans(self, file_path):
        """Import fans/customers from Excel"""
        self.stdout.write('\n[*] Importing fans/customers...')
        
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except:
            df = pd.read_excel(file_path, engine='xlrd')
        
        for idx, row in df.iterrows():
            fan_id = int(row.get('Fan_id', idx + 1))
            name = str(row.get('name', f'Fan {fan_id}')).strip()
            email = str(row.get('email', f'fan{fan_id}@example.com')).strip()
            country = str(row.get('country', '')).strip() if pd.notna(row.get('country')) else ''
            
            # Split name
            name_parts = name.split()
            first_name = name_parts[0] if name_parts else 'Fan'
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else str(fan_id)
            
            # Create Django user
            username = f'fan{fan_id}'
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            
            if user_created:
                user.set_password('fan123')
                user.save()
            
            # Create customer
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={
                    'country': country,
                }
            )
            
            if created:
                self.stdout.write(f'  [+] Created fan: {name} ({username})')
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] Imported {Customer.objects.count()} fans'))

    @transaction.atomic
    def import_events(self, file_path):
        """Import events from Excel"""
        self.stdout.write('\n[*] Importing events...')
        
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except:
            df = pd.read_excel(file_path, engine='xlrd')
        
        # Create default venue and event type
        concert_type, _ = EventType.objects.get_or_create(
            name='Concert',
            defaults={'description': 'Live concert performance'}
        )
        
        for _, row in df.iterrows():
            artist_id = row.get('artist_id')
            try:
                artist = Artist.objects.all()[int(artist_id) - 1] if pd.notna(artist_id) else None
            except (IndexError, ValueError):
                self.stdout.write(self.style.WARNING(f'  [!] Artist ID {artist_id} not found'))
                continue
            
            event_date = pd.to_datetime(row.get('date')).date() if pd.notna(row.get('date')) else timezone.now().date()
            location = str(row.get('location', 'TBD')).strip()
            
            # Create or get venue from location
            venue, _ = Venue.objects.get_or_create(
                name=f'{location} Venue',
                defaults={'location': location, 'capacity': 5000}
            )
            
            event, created = Event.objects.update_or_create(
                name=str(row['name']).strip(),
                date=event_date,
                defaults={
                    'description': f'Live performance by {artist.name}',
                    'venue': venue,
                    'event_type': concert_type,
                    'status': 'upcoming' if event_date > timezone.now().date() else 'completed',
                }
            )
            
            # Create performance relationship
            Performs.objects.get_or_create(
                artist=artist,
                event=event
            )
            
            if created:
                self.stdout.write(f'  [+] Created event: {event.name}')
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] Imported {Event.objects.count()} events'))

    @transaction.atomic
    def import_fan_interactions(self, file_path):
        """Import fan interactions from Excel"""
        self.stdout.write('\n[*] Importing fan interactions...')
        
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except:
            df = pd.read_excel(file_path, engine='xlrd')
        
        count = 0
        for _, row in df.iterrows():
            fan_id = int(row.get('Fan_id', 0))
            track_id = int(row.get('track_id', 0))
            
            try:
                fan = Customer.objects.all()[fan_id - 1] if fan_id > 0 else None
                track = Track.objects.all()[track_id - 1] if track_id > 0 else None
                
                if not fan or not track:
                    continue
                
                interaction_type = str(row.get('type of interaction', 'play')).lower().strip()
                # Map interaction types
                type_mapping = {
                    'play': 'play',
                    'like': 'like',
                    'share': 'share',
                    'download': 'download',
                    'playlist': 'playlist_add',
                }
                interaction_type = type_mapping.get(interaction_type, 'play')
                
                timestamp = pd.to_datetime(row.get('time_stamp'))
                if pd.notna(timestamp):
                    if not timezone.is_aware(timestamp):
                        timestamp = timezone.make_aware(timestamp)
                else:
                    timestamp = timezone.now()
                
                interaction, created = FanInteraction.objects.get_or_create(
                    fan=fan,
                    track=track,
                    timestamp=timestamp,
                    interaction_type=interaction_type,
                )
                
                if created:
                    count += 1
                    
            except (IndexError, ValueError) as e:
                continue
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] Imported {count} fan interactions'))

    def print_summary(self):
        """Print import summary"""
        self.stdout.write(self.style.SUCCESS('\n[SUMMARY] Import Summary:'))
        self.stdout.write(f'  - Genres: {Genre.objects.count()}')
        self.stdout.write(f'  - Artists: {Artist.objects.count()}')
        self.stdout.write(f'  - Albums: {Album.objects.count()}')
        self.stdout.write(f'  - Tracks: {Track.objects.count()}')
        self.stdout.write(f'  - Events: {Event.objects.count()}')
        self.stdout.write(f'  - Venues: {Venue.objects.count()}')
        self.stdout.write(f'  - Fans/Customers: {Customer.objects.count()}')
        self.stdout.write(f'  - Fan Interactions: {FanInteraction.objects.count()}')
        self.stdout.write(f'  - Bookings: {Booking.objects.count()}')
        self.stdout.write(f'  - Tickets: {Ticket.objects.count()}')
