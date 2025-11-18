from django.contrib import admin
from .models import Genre, Artist, Album, Track


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'genre', 'followers', 'popularity', 'is_active', 'created_at']
    list_filter = ['genre', 'is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'contact_email']
    list_editable = ['is_active']
    ordering = ['first_name', 'last_name']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['album_name', 'artist', 'release_date', 'total_tracks', 'created_at']
    list_filter = ['artist', 'release_date']
    search_fields = ['album_name', 'artist__first_name', 'artist__last_name']
    autocomplete_fields = ['artist']
    ordering = ['-release_date']


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['track_name', 'album', 'track_number', 'duration_formatted', 'created_at']
    list_filter = ['album__artist', 'album']
    search_fields = ['track_name', 'album__album_name', 'album__artist__first_name', 'album__artist__last_name']
    autocomplete_fields = ['album']
    ordering = ['album', 'track_number']