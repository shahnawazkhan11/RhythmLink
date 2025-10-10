from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class EventType(models.Model):
    """Types of events like concert, festival, etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Venue(models.Model):
    """Venue information"""
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    amenities = models.JSONField(default=list, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}"
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city', 'is_active']),
        ]


class Event(models.Model):
    """Main event information"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name='events')
    artists = models.ManyToManyField('artists.Artist', through='Performs', related_name='events')
    poster_image = models.ImageField(upload_to='event_posters/', blank=True, null=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)  # Base price
    max_tickets_per_customer = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def available_tickets_count(self):
        """Calculate available tickets"""
        from customers.models import Ticket
        return self.tickets.filter(status='available').count()
    
    @property
    def booking_percentage(self):
        """Calculate current booking percentage"""
        total_tickets = self.tickets.count()
        if total_tickets == 0:
            return 0
        booked_tickets = self.tickets.filter(status='booked').count()
        return (booked_tickets / total_tickets) * 100
    
    def __str__(self):
        return f"{self.name} - {self.date}"
    
    class Meta:
        ordering = ['date', 'start_time']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['date', 'is_active']),
            models.Index(fields=['venue', 'date']),
        ]


class Performs(models.Model):
    """Artist performance relationship with timing"""
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    performance_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    is_headliner = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.artist.name} at {self.event.name}"
    
    class Meta:
        unique_together = ['artist', 'event']
        ordering = ['performance_time']


class EventManager(models.Model):
    """Event managers who can manage events and pricing"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    contact_phone = models.CharField(max_length=20, blank=True)
    managed_events = models.ManyToManyField(Event, related_name='managers', blank=True)
    can_manage_pricing = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Manager: {self.user.get_full_name() or self.user.username}"
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]
