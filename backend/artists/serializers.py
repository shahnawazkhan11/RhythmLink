from rest_framework import serializers
from .models import Genre, Artist


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'created_at']


class ArtistSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = [
            'id', 'first_name', 'last_name', 'name', 'genre', 'genre_name', 'contact_email', 
            'contact_phone', 'bio', 'image', 'social_media_links',
            'is_active', 'created_at', 'updated_at'
        ]
    
    def get_name(self, obj):
        """Return full name for backward compatibility"""
        return f"{obj.first_name} {obj.last_name}".strip() if obj.last_name else obj.first_name