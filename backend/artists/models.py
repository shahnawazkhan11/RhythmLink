from django.db import models


class Genre(models.Model):
    """Music genre classification"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Artist(models.Model):
    """Artist/Band information"""
    name = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='artists')
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)
    
    # Fields from Excel data
    followers = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)  # 0-100 scale
    
    social_media_links = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),  # For search functionality
            models.Index(fields=['genre', 'is_active']),
            models.Index(fields=['-popularity']),  # For popular artists
        ]


class Album(models.Model):
    """Artist albums"""
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    album_name = models.CharField(max_length=200)
    release_date = models.DateField()
    total_tracks = models.IntegerField(default=0)
    
    # Additional fields
    cover_image = models.ImageField(upload_to='albums/', blank=True, null=True)
    description = models.TextField(blank=True)
    spotify_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.album_name} - {self.artist.name}"
    
    class Meta:
        ordering = ['-release_date']
        indexes = [
            models.Index(fields=['artist', '-release_date']),
            models.Index(fields=['album_name']),
        ]
        unique_together = [['artist', 'album_name']]


class Track(models.Model):
    """Individual tracks/songs"""
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    track_number = models.IntegerField()
    track_name = models.CharField(max_length=200)
    duration_ms = models.IntegerField(help_text="Duration in milliseconds")
    
    # Additional fields
    spotify_url = models.URLField(blank=True)
    preview_url = models.URLField(blank=True)
    is_explicit = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def duration_formatted(self):
        """Return duration as MM:SS"""
        total_seconds = self.duration_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def __str__(self):
        return f"{self.track_number}. {self.track_name}"
    
    class Meta:
        ordering = ['album', 'track_number']
        indexes = [
            models.Index(fields=['album', 'track_number']),
            models.Index(fields=['track_name']),
        ]
        unique_together = [['album', 'track_number']]