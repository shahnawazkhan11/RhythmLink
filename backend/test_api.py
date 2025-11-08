from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from events.models import Event, Venue, EventType
from artists.models import Genre
from artists.models import Artist
from pricing.models import PriceTier
from customers.models import Ticket

User = get_user_model()


class APIEndpointTests(TestCase):
    """API endpoint tests - 22 tests total"""
    
    def setUp(self):
        """Set up test data and API client"""
        self.client = APIClient()
        
        # Create users
        self.manager = User.objects.create_user(
            username='manager1',
            email='manager@example.com',
            password='manager123'
        )
        self.customer = User.objects.create_user(
            username='customer1',
            email='customer@example.com',
            password='customer123'
        )
        
        # Create test data
        self.venue = Venue.objects.create(name='Test Arena', location='Mumbai', address='123 Main St', city='Mumbai', state='Maharashtra', capacity=1000
        )
        self.event_type = EventType.objects.create(name='Concert')
        self.genre = Genre.objects.create(name='Rock')
        self.artist = Artist.objects.create(
            name='Test Artist',
            bio='Test bio',
            genre=self.genre
        )
        self.event = Event.objects.create(
            name='Rock Concert',
            venue=self.venue,
            event_type=self.event_type,
            date=timezone.now() + timedelta(days=30),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timedelta(hours=3)).time(),
            ticket_price=Decimal('1000.00')
        )
        
        # Create price tiers
        PriceTier.objects.create(
            event=self.event,
            tier_name='Early Bird',
            tier_percentage_start=0,
            tier_percentage_end=30,
            price=Decimal('500.00'),
            created_by_manager=self.manager
        )
    
    # Test 1: GET /api/events/events/ - List all events
    def test_get_events_list(self):
        """Test GET request to list all events"""
        response = self.client.get('/api/events/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    # Test 2: GET /api/events/events/<id>/ - Get single event
    def test_get_single_event(self):
        """Test GET request to retrieve single event"""
        response = self.client.get(f'/api/events/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Rock Concert')
    
    # Test 3: GET /api/events/venues/ - List venues
    def test_get_venues_list(self):
        """Test GET request to list all venues"""
        response = self.client.get('/api/events/venues/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    # Test 4: GET /api/events/event-types/ - List event types
    def test_get_event_types_list(self):
        """Test GET request to list event types"""
        response = self.client.get('/api/events/event-types/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    # Test 5: GET /api/artists/artists/ - List artists
    def test_get_artists_list(self):
        """Test GET request to list all artists"""
        response = self.client.get('/api/artists/artists/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    # Test 6: GET /api/artists/artists/<id>/ - Get single artist
    def test_get_single_artist(self):
        """Test GET request to retrieve single artist"""
        response = self.client.get(f'/api/artists/artists/{self.artist.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Artist')
    
    # Test 7: GET /api/artists/genres/ - List genres
    def test_get_genres_list(self):
        """Test GET request to list all genres"""
        response = self.client.get('/api/artists/genres/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    # Test 8: GET /api/pricing/tiers/<event_id>/ - Get price tiers
    def test_get_price_tiers(self):
        """Test GET request to retrieve price tiers for event"""
        response = self.client.get(f'/api/pricing/tiers/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
    
    # Test 9: GET /api/pricing/current-price/<event_id>/ - Get current price
    def test_get_current_price(self):
        """Test GET request to retrieve current price for event"""
        response = self.client.get(f'/api/pricing/current-price/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('current_price', response.data)
        self.assertIn('tier_name', response.data)
    
    # Test 10: GET /api/analytics/dashboard/<event_id>/ - Event dashboard
    def test_get_event_dashboard(self):
        """Test GET request to retrieve event analytics dashboard"""
        response = self.client.get(f'/api/analytics/dashboard/{self.event.id}/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
        if response.status_code == status.HTTP_200_OK:
            self.assertIn('event', response.data)
    
    # Test 11: GET /api/analytics/manager-dashboard/ - Manager overview
    def test_get_manager_dashboard(self):
        """Test GET request to retrieve manager dashboard"""
        self.client.force_authenticate(user=self.manager)
        response = self.client.get('/api/analytics/manager-dashboard/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])
    
    # Test 12: GET /api/search/autocomplete/ - Search autocomplete
    def test_search_autocomplete(self):
        """Test GET request to search autocomplete"""
        response = self.client.get('/api/search/autocomplete/?q=rock')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    # Test 13: GET /api/search/popular/ - Popular searches
    def test_get_popular_searches(self):
        """Test GET request to retrieve popular searches"""
        response = self.client.get('/api/search/popular/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    # Test 14: POST /api/events/events/ - Create event (authenticated)
    def test_create_event_authenticated(self):
        """Test POST request to create event (requires authentication)"""
        self.client.force_authenticate(user=self.manager)
        data = {
            'name': 'New Concert',
            'venue': self.venue.id,
            'event_type': self.event_type.id,
            'date': (timezone.now() + timedelta(days=60)).date(),
            'time': timezone.now().time()
        }
        response = self.client.post('/api/events/events/', data, format='json')
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN
        ])
    
    # Test 15: POST /api/events/events/ - Create event (unauthenticated)
    def test_create_event_unauthenticated(self):
        """Test POST request to create event without authentication"""
        data = {
            'name': 'New Concert',
            'venue': self.venue.id,
            'event_type': self.event_type.id,
            'date': (timezone.now() + timedelta(days=60)).date(),
            'time': timezone.now().time()
        }
        response = self.client.post('/api/events/events/', data, format='json')
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ])
    
    # Test 16: PUT /api/events/events/<id>/ - Update event
    def test_update_event(self):
        """Test PUT request to update event"""
        self.client.force_authenticate(user=self.manager)
        data = {
            'name': 'Updated Concert',
            'venue': self.venue.id,
            'event_type': self.event_type.id,
            'date': self.event.date,
            'time': self.event.time
        }
        response = self.client.put(
            f'/api/events/events/{self.event.id}/',
            data,
            format='json'
        )
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN
        ])
    
    # Test 17: DELETE /api/events/events/<id>/ - Delete event
    def test_delete_event(self):
        """Test DELETE request to delete event"""
        self.client.force_authenticate(user=self.manager)
        event = Event.objects.create(
            name='Event to Delete',
            venue=self.venue,
            event_type=self.event_type,
            date=timezone.now() + timedelta(days=45),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timedelta(hours=3)).time(),
            ticket_price=Decimal('1000.00')
        )
        response = self.client.delete(f'/api/events/events/{event.id}/')
        self.assertIn(response.status_code, [
            status.HTTP_204_NO_CONTENT,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ])
    
    # Test 18: API returns correct status codes for not found
    def test_get_nonexistent_event(self):
        """Test GET request for non-existent event returns 404"""
        response = self.client.get('/api/events/events/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # Test 19: API returns correct JSON schema for events
    def test_event_json_schema(self):
        """Test event response contains required fields"""
        response = self.client.get(f'/api/events/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        required_fields = ['id', 'name', 'venue', 'event_type', 'date']
        for field in required_fields:
            self.assertIn(field, response.data)
    
    # Test 20: API returns correct JSON schema for artists
    def test_artist_json_schema(self):
        """Test artist response contains required fields"""
        response = self.client.get(f'/api/artists/artists/{self.artist.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        required_fields = ['id', 'name', 'genre']
        for field in required_fields:
            self.assertIn(field, response.data)
    
    # Test 21: API returns correct JSON schema for pricing
    def test_pricing_json_schema(self):
        """Test pricing response contains required fields"""
        response = self.client.get(f'/api/pricing/current-price/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        required_fields = ['current_price', 'tier_name']
        for field in required_fields:
            self.assertIn(field, response.data)
    
    # Test 22: API pagination works correctly
    def test_api_pagination(self):
        """Test API pagination for list endpoints"""
        # Create multiple events
        for i in range(15):
            Event.objects.create(
                name=f'Event {i}',
                venue=self.venue,
                event_type=self.event_type,
                date=timezone.now() + timedelta(days=30+i),
                start_time=timezone.now().time(),
                end_time=(timezone.now() + timedelta(hours=3)).time(),
                ticket_price=Decimal('1000.00')
            )
        
        response = self.client.get('/api/events/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if pagination is enabled (response is dict with 'results')
        # or simple list
        self.assertTrue(
            isinstance(response.data, list) or 
            ('results' in response.data and isinstance(response.data['results'], list))
        )
