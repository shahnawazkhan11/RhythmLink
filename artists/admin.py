from django.contrib import admin
from .models import Genre, Artist


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'contact_email', 'is_active', 'created_at']
    list_filter = ['genre', 'is_active', 'created_at']
    search_fields = ['name', 'contact_email']
    list_editable = ['is_active']
    ordering = ['name']