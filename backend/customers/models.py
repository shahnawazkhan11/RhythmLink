from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(models.Model):
    """Customer profile extending Django User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Fields from Excel (Fans table)
    country = models.CharField(max_length=100, blank=True)
    
    preferred_genres = models.ManyToManyField('artists.Genre', blank=True)
    preferred_artists = models.ManyToManyField('artists.Artist', blank=True)
    marketing_consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['phone']),
            models.Index(fields=['country']),
        ]


class Ticket(models.Model):
    """Ticket information with dynamic pricing"""
    TICKET_STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.CharField(max_length=20, blank=True)
    section = models.CharField(max_length=50, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_tier = models.ForeignKey('pricing.PriceTier', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.event.name} - {self.seat_number}"
    
    class Meta:
        unique_together = ['event', 'seat_number']
        indexes = [
            models.Index(fields=['event', 'status']),
            models.Index(fields=['status']),
        ]


class Booking(models.Model):
    """Customer booking information"""
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='bookings')
    tickets = models.ManyToManyField(Ticket, related_name='bookings')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    payment_reference = models.CharField(max_length=100, blank=True)
    special_requests = models.TextField(blank=True)
    
    def __str__(self):
        return f"Booking {self.id} - {self.customer} - {self.event.name}"
    
    class Meta:
        indexes = [
            models.Index(fields=['customer', 'booking_date']),
            models.Index(fields=['event', 'status']),
            models.Index(fields=['booking_date']),
        ]


class Feedback(models.Model):
    """Customer feedback for events"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='feedback')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='feedback')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='feedback', null=True, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5 stars'
    )
    comment = models.TextField(blank=True)
    would_recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer} - {self.event.name} - {self.rating}★"
    
    class Meta:
        unique_together = ['customer', 'event']
        indexes = [
            models.Index(fields=['event', 'rating']),
            models.Index(fields=['created_at']),
        ]


class FanInteraction(models.Model):
    """Track fan interactions with songs/tracks"""
    INTERACTION_TYPES = [
        ('play', 'Play'),
        ('like', 'Like'),
        ('share', 'Share'),
        ('playlist_add', 'Added to Playlist'),
        ('download', 'Download'),
    ]
    
    fan = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    track = models.ForeignKey('artists.Track', on_delete=models.CASCADE, related_name='fan_interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    timestamp = models.DateTimeField()
    
    # Additional analytics fields
    device_type = models.CharField(max_length=50, blank=True)  # mobile, web, desktop
    location = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.fan} - {self.interaction_type} - {self.track.track_name}"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['fan', 'track', 'timestamp']),
            models.Index(fields=['track', '-timestamp']),
            models.Index(fields=['interaction_type', '-timestamp']),
        ]
        # Allow multiple interactions of same type at same time
        unique_together = [['fan', 'track', 'timestamp', 'interaction_type']]