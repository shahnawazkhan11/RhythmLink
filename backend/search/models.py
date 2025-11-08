from django.db import models
from django.contrib.auth.models import User


class SearchHistory(models.Model):
    """Track user search history for personalization"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history', null=True, blank=True)
    search_query = models.CharField(max_length=200)
    result_clicked = models.BooleanField(default=False)
    clicked_event = models.ForeignKey('events.Event', on_delete=models.SET_NULL, null=True, blank=True)
    clicked_artist = models.ForeignKey('artists.Artist', on_delete=models.SET_NULL, null=True, blank=True)
    clicked_venue = models.ForeignKey('events.Venue', on_delete=models.SET_NULL, null=True, blank=True)
    search_timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        user_info = self.user.username if self.user else "Anonymous"
        return f"{user_info}: {self.search_query}"
    
    class Meta:
        ordering = ['-search_timestamp']
        indexes = [
            models.Index(fields=['user', 'search_timestamp']),
            models.Index(fields=['search_query']),
        ]


class PopularSearches(models.Model):
    """Track popular search terms"""
    keyword = models.CharField(max_length=200, unique=True)
    search_count = models.PositiveIntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.keyword} ({self.search_count})"
    
    class Meta:
        ordering = ['-search_count']
        verbose_name_plural = "Popular Searches"