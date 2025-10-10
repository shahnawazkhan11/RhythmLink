from rest_framework import serializers
from .models import Genre, Artist


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'created_at']


class ArtistSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    
    class Meta:
        model = Artist
        fields = [
            'id', 'name', 'genre', 'genre_name', 'contact_email', 
            'contact_phone', 'bio', 'image', 'social_media_links',
            'is_active', 'created_at', 'updated_at'
        ]